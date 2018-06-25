import argparse, json, os, sys

from agithub.GitHub import GitHub
from agithub.base import IncompleteRequest
import ldap

# USAGE:
#   export GITHUB_API_TOKEN=...
#   export LDAP_URL=...
#   export LDAP_DC=...
#   export LDAP_BIND_USER=...
#   export LDAP_PASSWORD=...
#   ./activedirectory_github_sync.py voyages-sncf-technologies org_members.json

def main():
    args = parse_args()
    ad_client = ActiveDirectoryClient(args)
    ag = GitHubAPIWrapper(token=args.github_api_token)
    with open(args.login_mapping_file) as login_mapping_file:
        login_mapping = json.load(login_mapping_file)

    org_members = ag.orgs[args.org].members.get()
    for gh_login in set(org_members) - set(login_mapping.keys()):
        print('New GitHub user in org: {}'.format(gh_login), file=sys.stderr)
        login_mapping[gh_login] = ''
    for gh_login in set(login_mapping.keys()) - set(org_members):
        print('User removed from GitHub org: {}'.format(gh_login), file=sys.stderr)
        del login_mapping[gh_login]

    for gh_login, ad_login in login_mapping.items():
        if ad_login and not ad_client.retrieve_from_login(ad_login):
            print('User not in AD, REMOVED: {}/{}'.format(gh_login, ad_login), file=sys.stderr)
            del members[gh_login]

    with open(args.login_mapping_file, 'w') as login_mapping_file:
        json.dump(login_mapping, login_mapping_file)

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    parser.add_argument('org', help=' ')
    parser.add_argument('login_mapping_file', help=' ')
    parser.add_argument('--ignore_certs', action='store_true', help=' ')
    for var in ('GITHUB_API_TOKEN', 'LDAP_URL', 'LDAP_DC', 'LDAP_BIND_USER', 'LDAP_PASSWORD'):
        if var not in os.environ:
            raise EnvironmentError('The {} environment variable must be defined'.format(var))
        settattr(args, var.lower(), os.environ[var])
    return args


class ActiveDirectoryClient:
    def __init__(self, args):
        self.ldap_dc = args.ldap_dc
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        if args.ignore_certs:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        self.connection = ldap.initialize(args.ldap_url)
        self.connection.simple_bind_s('{},{}'.format(args.ldap_dc, args.ldap_bind_user), args.ldap_password)

    def retrieve_from_login(self, login):
        result = self.connection.search_s(self.ldap_dc, ldap.SCOPE_SUBTREE, 'sAMAccountName={}'.format(login))
        if len(result) < 4:
            return None
        return result


class GitHubAPIWrapper(GitHub):
    def __getattr__(self, key):
        return IncompleteRequestWrapper(self.client, self.ignore_403s).__getattr__(key)
    __getitem__ = __getattr__


class IncompleteRequestWrapper(IncompleteRequest):
    def __getattr__(self, key):
        result = super().__getattr__(key)
        if key in self.client.http_methods:
            return HTTPRequester(result)
        return result
    __getitem__ = __getattr__


class HTTPRequester:
    '''
    Callable, providing:
    - auto pages fetching when result count is > 100
    - raise exceptions on HTTP errors
    '''

    MAX_RESULTS_COUNT = 30

    def __init__(self, http_method_executer):
        self.http_method_executer = http_method_executer

    def __call__(self, *args, **kwargs):
        all_results, page = [], 1
        while len(all_results) % self.MAX_RESULTS_COUNT == 0:
            results = self._fetch(*args, page=page, **kwargs)
            if len(results) == 0:
                return all_results
            all_results.extend(results)
            page += 1
        return all_results

    def _fetch(self, *args, **kwargs):
        http_code, response = self.http_method_executer(*args, **kwargs)
        if http_code == 404:
            return []
        if http_code == 403 and self.ignore_403s:
            print('HTTP {}: {}'.format(http_code, response['message']), file=sys.stderr)
            return []
        if http_code != 200:
            raise RuntimeError('HTTP code: {}: {}'.format(http_code, response))
        return response


if __name__ == '__main__':
    main()
