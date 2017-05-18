#!/usr/bin/env python3
# TODO: still sometimes hang forever
# Dead URLs checker
# USAGE:
# - for Shaarli: jq -r '.[].url' datastore.json | grep -Ev 'ftp://|javascript:' | ./crawl_dead_links_gevent.py
# - for Chrome: jq -r '..|objects|select(has("children")).children[].url//empty' Bookmarks | ./crawl_dead_links_gevent.py
# STDIN FORMAT: 1 URL per line
# STDOUT FORMAT: [HTTP status | Python exception] URL (for all non-OKs URLs)
# Note: I had to edit /etc/security/limits.conf in order to increase the nofile soft & hard limits for the user executing this script
from gevent import monkey, sleep
from gevent.pool import Pool
from greenlet import greenlet
monkey.patch_all(thread=False, select=False)
import html, json, sys
from collections import defaultdict
from requests import Session
from requests.packages import urllib3
from urllib.parse import urlparse
from crawler_utils import error2str, robots_txt_url, robot_can_fetch, USER_AGENT
from perf_utils import compute_timing_stats, perf_counter


class PerHostAsyncRequests: # inspired by grequests
    def __init__(self, urls):
        self.urls = urls
        self.session = Session()
    def send(self):
        try:
            resp = self.session.get(robots_txt_url(self.urls[0]), verify=False)
            resp.raise_for_status()
            robots_txt_content = resp.text
        except BaseException as error:
            robots_txt_content = ''
        resps = []
        for url in self.urls:
            if robots_txt_content and not robot_can_fetch(robots_txt_content, url):
                resps.append((url, 'ROBOT FORBIDDEN', None, None))
                continue
            if resps:
                sleep(2) # rate-limiting 1 request every 2s per hostname
            start = perf_counter()
            try:
                response = self.session.get(url, verify=False, headers={'User-Agent': USER_AGENT})  # default requests UA is often blacklisted: https://github.com/kennethreitz/requests/blob/master/requests/utils.py#L731
                resps.append((url, response.status_code, perf_counter() - start, response.elapsed.total_seconds()))
            except Exception as error:
                resps.append((url, error2str(error), perf_counter() - start, None))
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


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    urls = set(html.unescape(url.strip()) for url in sys.stdin.readlines())
    count = 0
    perf_timings, elasped_timings = {}, {}
    progress_step = len(urls) // 10
    start = perf_counter()
    for url, status_or_error, exec_duration, elasped_req_time, pool_length in url_checker(urls):
        if exec_duration:
            perf_timings[url] = exec_duration
        if elasped_req_time != None:
            elasped_timings[url] = elasped_req_time
        count += 1
        # Looks like the following print statements do not get flushed to stdout before the end
        if status_or_error != 200:
            print(status_or_error, url) # this won't be displayed if there are too few URLs (too fast ?)
        if progress_step and count % progress_step == 0:
            print('#> {:.1f}% processed : count={} len(pool)={}'.format(count * 100.0 / len(urls), count, pool_length), file=sys.stderr)
    print('#= Done in', perf_counter() - start, file=sys.stderr)
    for name, timings in (('perf', perf_timings), ('requests', elasped_timings)):
        print('# {} timing stats:'.format(name), file=sys.stderr)
        print(json.dumps(compute_timing_stats(timings.values()), indent=4), file=sys.stderr)
        print('## Top10 slow requests:', file=sys.stderr)
        top_slow_urls = sorted(timings.keys(), key=timings.get)[-10:]
        print('\n'.join('- {} : {:.2f}s'.format(url, timings[url]) for url in top_slow_urls), file=sys.stderr)
