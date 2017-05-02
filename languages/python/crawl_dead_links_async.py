#!/usr/bin/python3
# Dead URLs checker
# USAGE:
# - for Shaarli: jq -r '.[].url' datastore.json | grep -Ev 'ftp://|javascript:' | ./crawl_dead_links.py
# - for Chrome: jq -r '..|objects|select(has("children")).children[].url//empty' Bookmarks | ./crawl_dead_links.py
# STDIN FORMAT: 1 URL per line
# STDOUT FORMAT: [HTTP status | Python exception] URL (for all non-OKs URLs)
# Note: I had to edit /etc/security/limits.conf in order to increase the nofile soft & hard limits for the user executing this script
from gevent import monkey, sleep
from gevent.pool import Pool
from greenlet import greenlet
monkey.patch_all(thread=False, select=False)
import json, sys
from collections import defaultdict
from datetime import datetime
from requests import Session
from requests.packages import urllib3
from urllib.parse import urlparse
from time import perf_counter

async def fetch(client, url):
    async with client.get(url) as resp:
        return await resp.status

async def check_urls(urls, checker_results, total_urls_count):
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        resps = []
        for url in urls:
            if resps:
                sleep(2) # rate-limiting 1 request every 2s per hostname
            start = perf_counter()
            try:
                response = await session.get(url, verify=False)
                resps.append((url, response.status, perf_counter() - start))
            except Exception as error:
                resps.append((url, error, perf_counter() - start))
        checker_results.extend(resps)
        count = len(checker_results)
        if count % (total_urls_count // 10) == 0:
            print('#> 10% more processed : count={}'.format(count), file=sys.stderr)

def url_checker(urls):
    urls_per_host = defaultdict(list)
    for url in urls:
        urls_per_host[urlparse(url).hostname].append(url)
    #import json; print(json.dumps({host: urls for host, urls in urls_per_host.items() if len(urls)>1}, indent=4), file=sys.stderr)
    checker_results = []
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            *(check_urls(one_host_urls, checker_results, len(urls)) for one_host_urls in urls_per_host.values())
        )
    )
    return checker_results

def compute_timing_stats(timings_in_ms):
    if not timings_in_ms:
        return {'count': 0}
    timings_in_ms = sorted(timings_in_ms)
    total = sum(timings_in_ms)
    return {
        'count': len(timings_in_ms),
        'mean': total / len(timings_in_ms),
        'p00_min': timings_in_ms[0],
        'p01': percentile(timings_in_ms, .01),
        'p10': percentile(timings_in_ms, .1),
        'p50_median': percentile(timings_in_ms, .5),
        'p90': percentile(timings_in_ms, .9),
        'p99': percentile(timings_in_ms, .99),
        'p100_max': timings_in_ms[-1],
        'pstdev': statistics.pstdev(timings_in_ms),
        'sum': total
     }

if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    urls = [url.strip() for url in sys.stdin.readlines()]
    start = datetime.utcnow()
    timings = {}
    for url, status_or_error, exec_duration in url_checker(urls):
        timings[url] = exec_duration
        if status_or_error != 200:
            print(status_or_error, url) # this won't be displayed if there are too few URLs (too fast ?)
    end = datetime.utcnow()
    print('#= Done in', end - start, file=sys.stderr)
    print(json.dumps(compute_timing_stats(timings.values()), indent=4), file=sys.stderr)
    print('Top10 slow requests:', file=sys.stderr)
    top_slow_urls = sorted(timings.keys(), key=timings.get)[-10:]
    print('\n'.join('- {} : {}s'.format(url, timings[url]) for url in top_slow_urls), file=sys.stderr)
