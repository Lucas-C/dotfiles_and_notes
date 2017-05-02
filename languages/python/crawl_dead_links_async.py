#!/usr/local/bin/python3.5
# Dead URLs checker
# USAGE:
# - for Shaarli: jq -r '.[].url' datastore.json | grep -Ev 'ftp://|javascript:' | ./crawl_dead_links.py
# - for Chrome: jq -r '..|objects|select(has("children")).children[].url//empty' Bookmarks | ./crawl_dead_links.py
# STDIN FORMAT: 1 URL per line
# STDOUT FORMAT: [HTTP status | Python exception] URL (for all non-OKs URLs)
# Note: I had to edit /etc/security/limits.conf in order to increase the nofile soft & hard limits for the user executing this script
import asyncio, aiohttp, json, statistics, sys
from collections import defaultdict
from datetime import datetime
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
                asyncio.sleep(2) # rate-limiting 1 request every 2s per hostname
            start = perf_counter()
            try:
                async with session.get(url, verify=False) as response:
                    resps.append((url, response.status, perf_counter() - start))
            except Exception as error:
                resps.append((url, error, perf_counter() - start))
        checker_results.extend(resps)
        count = len(checker_results)
        if count % (total_urls_count // 10) == 0:
            print('#> {:.1f}% processed : count={}'.format(count * 100.0 / total_urls_count, count), file=sys.stderr)

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

def percentile(sorted_data, percent):
    assert 0 <= percent < 1
    index = (len(sorted_data)-1) * percent
    return sorted_data[int(index)]

if __name__ == '__main__':
    urls = [url.strip() for url in sys.stdin.readlines()]
    start = datetime.utcnow()
    timings = {}
    for url, status_or_error, exec_duration in url_checker(urls):
        timings[url] = exec_duration
        if status_or_error != 200:
            print(status_or_error, url)
    end = datetime.utcnow()
    print('#= Done in', end - start, file=sys.stderr)
    print(json.dumps(compute_timing_stats(timings.values()), indent=4), file=sys.stderr)
    print('Top10 slow requests:', file=sys.stderr)
    top_slow_urls = sorted(timings.keys(), key=timings.get)[-10:]
    print('\n'.join('- {} : {:.1f}s'.format(url, timings[url]) for url in top_slow_urls), file=sys.stderr)
