#!/usr/bin/env python3.5
# Dead URLs checker
# USAGE:
# - for Shaarli: jq -r '.[].url' datastore.json | grep -Ev 'ftp://|javascript:' | ./crawl_dead_links_asyncio.py
# - for Chrome: jq -r '..|objects|select(has("children")).children[].url//empty' Bookmarks | ./crawl_dead_links_asyncio.py
# STDIN FORMAT: 1 URL per line
# STDOUT FORMAT: [HTTP status | Python exception] URL (for all non-OKs URLs)
# TODO:
# - test https://github.com/gaojiuli/gain
# - rate-limit like this ? https://quentin.pradet.me/blog/how-do-you-rate-limit-calls-with-asyncio.html
import asyncio as aio, aiohttp, html, json, sys
from async_timeout import timeout
from collections import defaultdict
from datetime import datetime
from urllib.parse import urlparse
from crawler_utils import error2str, robots_txt_url, robot_can_fetch, USER_AGENT
from perf_utils import compute_timing_stats, perf_counter


async def check_one_host_urls(client, queue, urls):
    try:
        async with client.get(robots_txt_url(urls[0]), raise_for_status=True) as response:
            robots_txt_content = await response.text()
    except Exception:
        robots_txt_content = ''
    resps = []
    for url in urls:
        if robots_txt_content and not robot_can_fetch(robots_txt_content, url):
            resps.append((url, 'ROBOT FORBIDDEN', None))
            continue
        if resps:
            aio.sleep(2) # rate-limiting 1 request every 2s per hostname
        try:
            start = perf_counter()
            async with client.get(url, timeout=60) as response:
                resps.append((url, response.status, perf_counter() - start))
        except Exception as error:
            resps.append((url, error2str(error), perf_counter() - start))
    await queue.put(resps)

async def check_all_urls(urls, checker_results):
    urls_per_host = defaultdict(list)
    for url in urls:
        urls_per_host[urlparse(url).hostname].append(url)
    #print(json.dumps({host: urls for host, urls in urls_per_host.items() if len(urls)>1}, indent=4), file=sys.stderr)
    progress_step = len(urls) // 10
    queue = aio.Queue()
    async with aiohttp.ClientSession(raise_for_status=True, connector=aiohttp.TCPConnector(verify_ssl=False, limit=100), headers = {'User-Agent': USER_AGENT}) as client:
    # default UA: https://github.com/aio-libs/aiohttp/blob/master/aiohttp/http.py#L34
        aio.gather(check_one_host_urls(client, queue, one_host_urls) for one_host_urls in urls_per_host.values())
        start = perf_counter()
        with timeout(20*60):
            for _ in range(len(urls_per_host)):
                resps = await queue.get()
                checker_results.extend(resps)
                count = len(checker_results)
                if progress_step and count % progress_step == 0: # those do not get printed progressively :(
                    print('#> {:.1f}% processed : count={} time={}'.format(count * 100.0 / len(urls), count, perf_counter() - start), file=sys.stderr)

def url_checker(urls):
    checker_results = []
    loop = aio.get_event_loop()
    loop.set_debug(True)
    loop.slow_callback_duration = 1 # seconds
    try:
        loop.run_until_complete(check_all_urls(urls, checker_results))
    except aio.TimeoutError:
        unprocessed_urls = set(urls) - set(resp[0] for resp in checker_results)
        print('20min TIMEOUT', file=sys.stderr)
        print(unprocessed_urls, file=sys.stderr)
    return checker_results


if __name__ == '__main__':
    urls = set(html.unescape(url.strip()) for url in sys.stdin.readlines())
    timings = {}
    start = perf_counter()
    for url, status_or_error, exec_duration in url_checker(urls):
        if exec_duration:
            timings[url] = exec_duration
        if status_or_error != 200:
            print(str(status_or_error) or type(status_or_error), status_or_error, url)
    print('#= Done in', perf_counter() - start, file=sys.stderr)
    print('# perf timing stats:', file=sys.stderr)
    print(json.dumps(compute_timing_stats(timings.values()), indent=4), file=sys.stderr)
    print('## Top10 slow requests:', file=sys.stderr)
    top_slow_urls = sorted(timings.keys(), key=timings.get)[-10:]
    print('\n'.join('- {} : {:.2f}s'.format(url, timings[url]) for url in top_slow_urls), file=sys.stderr)
