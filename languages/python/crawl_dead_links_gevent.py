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
import json, statistics, sys
from collections import defaultdict
from datetime import datetime
from requests import Session
from requests.packages import urllib3
from urllib.parse import urlparse
from time import perf_counter

class PerHostAsyncRequests: # inspired by grequests
    def __init__(self, urls):
        self.urls = urls
        self.session = Session()
    def send(self):
        resps = []
        for url in self.urls:
            if resps:
                sleep(2) # rate-limiting 1 request every 2s per hostname
            start = perf_counter()
            try:
                response = self.session.get(url, verify=False)
                resps.append((url, response.status_code, perf_counter() - start, response.elapsed.total_seconds()))
            except Exception as error:
                resps.append((url, error, perf_counter() - start, None))
        return resps

def url_checker(urls):
    urls_per_host = defaultdict(list)
    for url in urls:
        urls_per_host[urlparse(url).hostname].append(url)
    #print(json.dumps({host: urls for host, urls in urls_per_host.items() if len(urls)>1}, indent=4), file=sys.stderr)

    reqs = (PerHostAsyncRequests(urls) for urls in urls_per_host.values())
    pool = Pool(size=None)
    for resps in pool.imap_unordered(lambda r: r.send(), reqs):
        for resp in resps:
            yield resp + (len(pool),)
    pool.join(raise_error=True)

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
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    urls = [url.strip() for url in sys.stdin.readlines()]
    start = datetime.utcnow()
    count = 0
    perf_timings, elasped_timings = {}, {}
    for url, status_or_error, exec_duration, pool_length, elasped_req_time in url_checker(urls):
        perf_timings[url] = exec_duration
        if elasped_req_time != None:
            elasped_timings[url] = elasped_req_time
        count += 1
        # Looks like the following print statements do not get flushed to stdout before the end
        if status_or_error != 200:
            print(status_or_error, url) # this won't be displayed if there are too few URLs (too fast ?)
        if count % (len(urls) // 10) == 0:
            print('#> {:.1f}% processed : count={} len(pool)={}'.format(count * 100.0 / len(urls), count, pool_length), file=sys.stderr)
    end = datetime.utcnow()
    print('#= Done in', end - start, file=sys.stderr)
    for name, timings in (('perf', perf_timings), ('requests', elasped_timings)):
        print('# {} timing stats:'.format(name), file=sys.stderr)
        print(json.dumps(compute_timing_stats(timings.values()), indent=4), file=sys.stderr)
        print('## Top10 slow requests:', file=sys.stderr)
        top_slow_urls = sorted(timings.keys(), key=timings.get)[-10:]
        print('\n'.join('- {} : {:.2f}s'.format(url, timings[url]) for url in top_slow_urls), file=sys.stderr)
