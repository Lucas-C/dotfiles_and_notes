#!/usr/bin/env python
'''
Script to ensure GitHub users in an organization
match the ones in an internal ActiveDirectory,
so that when enterprise members leave
they loose their rights on GitHub repos.

USAGE:
  pip install python-ldap requests
  export GITHUB_API_TOKEN=...
  export LDAP_URL=...
  export LDAP_BASE_DN=...
  export LDAP_BIND_USER=...
  export LDAP_BIND_PASSWORD=...
  ./activedirectory_github_sync.py voyages-sncf-technologies org_members.json

Notes:
* currently does not handle orgs with #members > 100,
  but this would just require adding support for pagination (trivial)
* this could easily be made into an AWS lambda function,
  with the JSON file stored on S3
'''
from __future__ import print_function
import argparse, json, os, sys

import ldap, requests
try:  # optional dependency
    from tqdm import tqdm
except ImportError:
    tqdm = lambda _: _


def main():
    args = parse_args()
    ad_client = ActiveDirectoryClient(args)
    session = requests.Session()
    session.auth = ('', args.github_api_token)
    try:
        with open(args.login_mapping_file) as login_mapping_file:
            login_mapping = json.load(login_mapping_file)
    except FileNotFoundError:
        login_mapping = {}

    resp = session.get(f'https://api.github.com/orgs/{args.org}/members', params={'per_page': 100})
    resp.raise_for_status()
    org_members = set(member['login'] for member in resp.json())
    new_gh_users = False
    for gh_login in org_members - set(login_mapping.keys()):
        print(f'New GitHub user detected in org: {gh_login}', file=sys.stderr)
        login_mapping[gh_login] = ''
        new_gh_users = True
        print('Looking for its email address to help figure their matching ActiveDirectory username...')
        user_email = get_user_emails(session, gh_login)
        if user_email:
            print('Associated user email found:', user_email)
        else:
            print('No user email could be found')
    if new_gh_users:
        print('Matching ActiveDirectory usernames will have to be manually added to the JSON mapping file')
    login_mapping_changed = new_gh_users
    for gh_login in set(login_mapping.keys()) - org_members:
        print(f'User removed from GitHub org: {gh_login}', file=sys.stderr)
        del login_mapping[gh_login]
        login_mapping_changed = True

    for gh_login, ad_login in list(login_mapping.items()):
        if ad_login and not ad_client.retrieve_from_login(ad_login):
            print(f'User not in AD, REMOVING: {gh_login}/{ad_login}', file=sys.stderr)
            if not args.dry_run:
                session.delete(f'https://api.github.com/orgs/{args.org}/members/{gh_login}').raise_for_status()
            login_mapping = {ghlogin: adlogin for ghlogin, adlogin in login_mapping.items() if ghlogin != gh_login}
            login_mapping_changed = True

    if not args.dry_run:
        with open(args.login_mapping_file, 'w') as login_mapping_file:
            json.dump(login_mapping, login_mapping_file, sort_keys=True, indent=4)
        if login_mapping_changed:
            print(f'{args.login_mapping_file} has been modified')


def get_user_emails(session, gh_login, stop_at_first_match=True):
    resp = session.get(f'https://api.github.com/users/{gh_login}/repos', params={'per_page': 100})
    resp.raise_for_status()
    repos = resp.json()
    emails = set()
    for repo in tqdm(repos):
        if repo['size'] == 0:
            continue  # avoids an HTTP 409 error
        resp = session.get(f'https://api.github.com/repos/{repo["full_name"]}/commits', params={'per_page': 100})
        resp.raise_for_status()
        for commit in resp.json():
            author = commit['author']
            if author and author['login'] == gh_login:
                email = commit['commit']['author']['email']
                if not email.endswith('@users.noreply.github.com'):
                    if stop_at_first_match:
                        return email
                    emails.add(email)
    # if no emails are found but the user uses an "@users.noreply.github.com" email address,
    # we could look for very old repos / commits
    return emails


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=ArgparseHelpFormatter,
                                     description=__doc__, allow_abbrev=False)
    parser.add_argument('org', help='GIthub organization name')
    parser.add_argument('login_mapping_file', help='A JSON file mapping GitHub usernames to LDAP usernames')
    parser.add_argument('--dry-run', action='store_true', help='Do not delete GitHub users not edit the JSON mapping file')
    parser.add_argument('--ignore-ldap-certs', action='store_true', help='Sets TLS_REQUIRE_CERT to NEVER')
    args = parser.parse_args()
    for var in ('GITHUB_API_TOKEN', 'LDAP_URL', 'LDAP_BASE_DN', 'LDAP_BIND_USER', 'LDAP_BIND_PASSWORD'):
        if var not in os.environ:
            raise EnvironmentError(f'The {var} environment variable must be defined')
        setattr(args, var.lower(), os.environ[var])
    return args

class ArgparseHelpFormatter(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


class ActiveDirectoryClient:
    def __init__(self, args):
        self.ldap_base_dn = args.ldap_base_dn
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        if args.ignore_ldap_certs:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        self.connection = ldap.initialize(args.ldap_url)
        self.connection.simple_bind_s(args.ldap_bind_user, args.ldap_bind_password)

    def retrieve_from_login(self, login):
        result = self.connection.search_s(self.ldap_base_dn, ldap.SCOPE_SUBTREE, 'sAMAccountName=' + login)
        if len(result) < 4:
            return None
        return result


if __name__ == '__main__':
    # print(get_user_emails(requests.Session(), 'Lucas-C'))
    main()
