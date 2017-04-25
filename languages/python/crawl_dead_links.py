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

from perf_utils import compute_timing_stats, trace_exec_time

class PerHostAsyncRequests: # inspired by grequests
    def __init__(self, urls):
        self.urls = urls
        self.session = Session()
    def send(self):
        resps = []
        for url in self.urls:
            if resps:
                sleep(2) # rate-limiting 1 request every 2s per hostname
            try:
                with trace_exec_time() as timer:
                    response = self.session.get(url, verify=False)
                resps.append((url, response.status_code, timer['exec_duration_in_ms']))
            except Exception as error:
                resps.append((url, error, timer['exec_duration_in_ms']))
        return resps

def url_checker(urls):
    urls_per_host = defaultdict(list)
    for url in urls:
        urls_per_host[urlparse(url).hostname].append(url)
    #import json; print(json.dumps({host: urls for host, urls in urls_per_host.items() if len(urls)>1}, indent=4), file=sys.stderr)

    reqs = (PerHostAsyncRequests(urls) for urls in urls_per_host.values())
    pool = Pool(size=None)
    for resps in pool.imap_unordered(lambda r: r.send(), reqs):
        for url, status_or_error, exec_duration in resps:
            yield url, status_or_error, exec_duration, len(pool)
    pool.join(raise_error=True)

if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    urls = [url.strip() for url in sys.stdin.readlines()]
    start = datetime.utcnow()
    count = 0
    timings = {}
    for url, status_or_error, exec_duration, pool_length in url_checker(urls):
        timings[url] = exec_duration
        count += 1
        # Looks like the following print statements do not get flushed to stdout before the end
        if status_or_error != 200:
            print(status_or_error, url) # this won't be displayed if there are too few URLs (too fast ?)
        if count % (len(urls) // 10) == 0:
            print('#> 10% more processed : count={} len(pool)={}'.format(count, pool_length), file=sys.stderr)
    end = datetime.utcnow()
    print('#= Done in', end - start, file=sys.stderr)
    print(json.dumps(compute_timing_stats(timings.values()), indent=4), file=sys.stderr)
    print('Top10 slow requests:', file=sys.stderr))
    top_slow_urls = sorted(timings.keys(), key=timings.get)[:10]
    print('\n'.join('- ' + url for url in top_slow_urls), file=sys.stderr))
