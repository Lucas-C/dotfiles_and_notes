#!/usr/local/bin/python3.5 -Wdefault
# Dead URLs checker
# USAGE:
# - for Shaarli: jq -r '.[].url' datastore.json | grep -Ev 'ftp://|javascript:' | ./crawl_dead_links.py
# - for Chrome: jq -r '..|objects|select(has("children")).children[].url//empty' Bookmarks | ./crawl_dead_links.py
# STDIN FORMAT: 1 URL per line
# STDOUT FORMAT: [HTTP status | Python exception] URL (for all non-OKs URLs)
import asyncio, aiohttp, sys
from collections import defaultdict
from datetime import datetime
from urllib.parse import urlparse

async def check_one_host_urls(client, queue, urls):
    resps = []
    for url in urls:
        if resps:
            asyncio.sleep(2) # rate-limiting 1 request every 2s per hostname
        try:
            async with client.get(url) as response:
                resps.append((url, response.status))
        except Exception as error:
            resps.append((url, error))
    await queue.put(resps)

async def check_all_urls(urls, checker_results):
    async with aiohttp.ClientSession(raise_for_status=True, connector=aiohttp.TCPConnector(verify_ssl=False, limit=100)) as client:
        urls_per_host = defaultdict(list)
        for url in urls:
            urls_per_host[urlparse(url).hostname].append(url)
        #import json; print(json.dumps({host: urls for host, urls in urls_per_host.items() if len(urls)>1}, indent=4), file=sys.stderr)
        queue = asyncio.Queue()
        for one_host_urls in urls_per_host.values():
            asyncio.ensure_future(check_one_host_urls(client, queue, one_host_urls))
        for _ in range(len(one_host_urls)):
            resps = await queue.get()
            checker_results.extend(resps)
            count = len(checker_results)
            if count % (len(urls) // 10) == 0:
                print('#> {:.1f}% processed : count={}'.format(count * 100.0 / len(urls), count), file=sys.stderr)

def url_checker(urls):
    checker_results = []
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.slow_callback_duration = 1 # seconds
    loop.run_until_complete(check_all_urls(urls, checker_results))
    return checker_results

if __name__ == '__main__':
    urls = [url.strip() for url in sys.stdin.readlines()]
    start = datetime.utcnow()
    for url, status_or_error in url_checker(urls):
        if status_or_error != 200:
            print(status_or_error, url)
    end = datetime.utcnow()
    print('#= Done in', end - start, file=sys.stderr)