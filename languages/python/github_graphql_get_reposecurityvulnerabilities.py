#!/usr/bin/env python3

# USAGE:
#   export GITHUB_OAUTH_TOKEN=...
#   ./github_graphql_get_reposecurityvulnerabilities.py --help

# Online explorer: https://developer.github.com/v4/explorer/

import argparse, json, os, requests, sys


GRAPHQL_QUERY = '''query($login:String!, $number_of_repos:Int!, $number_of_vulns:Int!, $next_cursor:String) {
  $org_or_user(login: $login) {
    repositories(first: $number_of_repos, after: $next_cursor) {  # for users, we could also use repositoriesContributedTo
      totalCount
      pageInfo {
        hasNextPage
        hasPreviousPage
        startCursor
        endCursor
      }
      nodes {
        name
        isArchived
        vulnerabilityAlerts(first: $number_of_vulns) {
          totalCount
          pageInfo {
            hasNextPage
            hasPreviousPage
            startCursor
            endCursor
          }
          nodes {
            createdAt
            vulnerableRequirements
            dismissedAt
            dismissReason
            securityVulnerability {
              advisory {
                description
                identifiers {
                  value
                }
              }
              severity
              package {
                ecosystem
                name
              }
              updatedAt
              vulnerableVersionRange
            }
          }
        }
      }
    }
  }
}'''


def main():
    args = parse_args()
    repos = query_graphql_api(args)
    print_alerts(args, repos['nodes'])
    while repos['pageInfo']['hasNextPage']:
        args.next_cursor = repos['pageInfo']['endCursor']
        repos = query_graphql_api(args)
        print_alerts(args, repos['nodes'])


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    parser.add_argument('--org', help=' ')
    parser.add_argument('--user', help=' ')
    parser.add_argument('--number-of-repos', type=int, default=100, help=' ')
    parser.add_argument('--number-of-vulns', type=int, default=100, help=' ')
    parser.add_argument('--only-urls', action='store_true', help=' ')
    parser.add_argument('--github-oauth-token', **in_env_or_required('GITHUB_OAUTH_TOKEN'))
    args = parser.parse_args()
    if not (args.org or args.user):
        parser.error('One of --user / --org must be provided')
    if args.org and args.user:
        parser.error('Only one of --user / --org must be provided')
    return args


def in_env_or_required(key):
    if os.environ.get(key):
        return {'default': os.environ.get(key)}
    return {'required': True}


def query_graphql_api(args):
    org_or_user = 'organization' if args.org else 'user'
    variables = vars(args)
    variables['login'] = args.org or args.user
    response = requests.post('https://api.github.com/graphql',
                             data=json.dumps({'query': GRAPHQL_QUERY.replace('$org_or_user', org_or_user), 'variables': variables}),
                             headers={'Authorization': 'bearer ' + args.github_oauth_token,  # cf. https://developer.github.com/v4/guides/forming-calls/#authenticating-with-graphql
                                      'Accept': 'application/vnd.github.vixen-preview+json'})  # cf. https://developer.github.com/v4/previews/#repository-vulnerability-alerts
    response.raise_for_status()
    print('X-RateLimit-Remaining:', response.headers['X-RateLimit-Remaining'], file=sys.stderr)
    if 'errors' in response.json():
        raise RuntimeError(response.text)
    return response.json()['data'][org_or_user]['repositories']


def print_alerts(args, nodes):
    for repo in nodes:
        if repo['vulnerabilityAlerts']['pageInfo']['hasNextPage']:
            raise RuntimeError('vulnerabilityAlerts are paginated over more than 1 page, and this script does not currently handle this')
        if repo['vulnerabilityAlerts']['nodes']:
            print('https://github.com/{}/{}/network/alerts'.format(args.org or args.user, repo['name']))
            if not args.only_urls:
                for alert in repo['vulnerabilityAlerts']['nodes']:
                    print(alert)


if __name__ == '__main__':
    main()
