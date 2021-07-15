#!/usr/bin/python3

# USAGE:
#   export GITHUB_OAUTH_TOKEN=...
#   ./get_github_repo_stats.py pulls toto/tata --closed-after 2019-01-01

# API DOC: https://developer.github.com/v3/issues/

import argparse, json, os, sys
from datetime import datetime

from agithub.GitHub import GitHub
from agithub.base import IncompleteRequest


def main():
    if 'GITHUB_OAUTH_TOKEN' not in os.environ:
        raise RuntimeError('Environment variable GITHUB_OAUTH_TOKEN must be defined')
    args = parse_args()
    ag = GitHubAPIWrapper(token=os.environ['GITHUB_OAUTH_TOKEN'])
    org, repo = args.org_repo.split('/')
    kwargs = {'labels': args.labels} if args.labels else {}
    issues = ag.repos[org][repo].issues.get(state='all', **kwargs)
    def filter_pull_or_issue(issue):
        return 'pull_request' in issue if args.pull_or_issue == 'pulls' else 'pull_request' not in issue
    issues = [issue for issue in issues if filter_pull_or_issue(issue)]
    if args.closed_after:
        issues = [issue for issue in issues if issue['closed_at'] and datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ') > args.closed_after]
    if args.closed_before:
        issues = [issue for issue in issues if issue['closed_at'] and datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ') < args.closed_before]
    if args.created_after:
        issues = [issue for issue in issues if datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ') > args.created_after]
    if args.created_before:
        issues = [issue for issue in issues if datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ') < args.created_before]
    print(json.dumps(issues, indent=2, sort_keys=True))


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    parser.add_argument('pull_or_issue', choices=('issues', 'pulls'))
    parser.add_argument('org_repo')
    parser.add_argument('--closed-after', type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    parser.add_argument('--closed-before', type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    parser.add_argument('--created-after', type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    parser.add_argument('--created-before', type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    parser.add_argument('--labels', help='Comma separated list')
    return parser.parse_args()


class GitHubAPIWrapper(GitHub):
    def __init__(self, *args, ignore_403s=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.ignore_403s = ignore_403s

    def __getattr__(self, key):
        return IncompleteRequestWrapper(self.client, self.ignore_403s).__getattr__(key)
    __getitem__ = __getattr__


class IncompleteRequestWrapper(IncompleteRequest):
    def __init__(self, client, ignore_403s):
        super().__init__(client)
        self.ignore_403s = ignore_403s

    def __getattr__(self, key):
        result = super().__getattr__(key)
        if key in self.client.http_methods:
            return HTTPRequester(result, self.ignore_403s)
        return result
    __getitem__ = __getattr__


class HTTPRequester:
    '''
    Callable, providing:
    - auto pages fetching when result count is > 100
    - raise exceptions on HTTP errors
    '''

    MAX_RESULTS_COUNT = 30

    def __init__(self, http_method_executer, ignore_403s):
        self.http_method_executer = http_method_executer
        self.ignore_403s = ignore_403s

    def __call__(self, *args, **kwargs):
        all_results, page = [], 1
        while len(all_results) % self.MAX_RESULTS_COUNT == 0:
            print('.', end='', file=sys.stderr)
            result = self._fetch(*args, page=page, **kwargs)
            if not isinstance(result, list):
                return result
            if len(result) == 0:
                return all_results
            all_results.extend(result)
            page += 1
        return all_results

    def _fetch(self, *args, **kwargs):
        http_code, response = self.http_method_executer(*args, **kwargs)
        if http_code == 403 and self.ignore_403s:
            print('HTTP {}: {}'.format(http_code, response['message']), file=sys.stderr)
            return []
        if http_code != 200:
            raise RuntimeError('HTTP code: {}: {}'.format(http_code, response))
        return response


if __name__ == '__main__':
    main()
