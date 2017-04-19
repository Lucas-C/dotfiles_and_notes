#!/usr/bin/python3
# Dead URLs checker
# USAGE:
# - for Shaarli: jq -r '.[].url' datastore.json | grep -Ev 'ftp://|javascript:' | ./crawl_dead_links.py
# - for Chrome: jq -r '..|objects|select(has("children")).children[].url//empty' Bookmarks | ./crawl_dead_links.py
# STDIN FORMAT: 1 URL per line
# STDOUT FORMAT: [HTTP status | Python exception] URL (for all non-OKs URLs)
# Note: I had to edit /etc/security/limits.conf in order to increase the nofile soft & hard limits for the user executing this script
from gevent import monkey, sleep
from gevent.pool import Pool as gPool
monkey.patch_all(thread=False, select=False)
import sys
from collections import defaultdict
from datetime import datetime
from requests import Session
from urllib.parse import urlparse

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
                response = self.session.get(url, verify=False)
                resps.append((url, response.status_code))
            except Exception as error:
                resps.append((url, error))
        return resps

def url_checker(urls):
    urls_per_host = defaultdict(list)
    for url in urls:
        urls_per_host[urlparse(url).hostname].append(url)
    #import json; print(json.dumps({host: urls for host, urls in urls_per_host.items() if len(urls)>1}, indent=4), file=sys.stderr)

    reqs = (PerHostAsyncRequests(urls) for urls in urls_per_host.values())
    pool = gPool(size=None)
    for resps in pool.imap_unordered(lambda r: r.send(), reqs):
        for url, status_or_error in resps:
            yield url, status_or_error, len(pool)
    pool.join()

if __name__ == '__main__':
    urls = sys.stdin.readlines()
    start = datetime.utcnow()
    count = 0
    for url, status_or_error, pool_length in url_checker(urls):
        count += 1
        # Looks like the following print statements do not get flushed to stdout before the end
        if status_or_error != 200:
            print(status_or_error, url)
        if count % (len(urls) // 10) == 0:
            print('#> 10% more processed : count={} len(pool)={}'.format(count, pool_length), file=sys.stderr)
    end = datetime.utcnow()
    print('#= Done in', end - start, file=sys.stderr)
