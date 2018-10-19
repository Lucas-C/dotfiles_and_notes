#!/usr/bin/python

# USAGE:
#   export GITHUB_OAUTH_TOKEN=...
#   ./github_graphql_get_reposecurityvulnerabilities.py

import json, os, requests, sys

MAX_FETCHED = 100

def main():
    graphql_query = '''query {
        viewer {
            login repositories(isFork: false, first: MAX_FETCHED) { # only fetching source repos
                nodes {
                    name
                    vulnerabilityAlerts(first: MAX_FETCHED) {
                        nodes {
                            packageName
                            affectedRange
                            externalReference
                            fixedIn
                        }
                    }
                }
            }
        }
    }'''.replace('MAX_FETCHED', str(MAX_FETCHED))  # not using str.format because of the numerous curly braces
    response = requests.post('https://api.github.com/graphql',
                             data=json.dumps({'query': graphql_query}),
                             headers={'Authorization': 'bearer ' + os.environ['GITHUB_OAUTH_TOKEN'],  # cf. https://developer.github.com/v4/guides/forming-calls/#authenticating-with-graphql
                                      'Accept': 'application/vnd.github.vixen-preview+json'})  # cf. https://developer.github.com/v4/previews/#repository-vulnerability-alerts
    response.raise_for_status()
    viewer_results = response.json()['data']['viewer']
    if len(viewer_results['repositories']['nodes']) == MAX_FETCHED:
        print('WARNING: You are hitting the max of {} repos fetched, while you probably have more, and pagination is currently not implemented'.format(MAX_FETCHED), file=sys.stderr)
    for repo in viewer_results['repositories']['nodes']:
        if not repo['vulnerabilityAlerts']['nodes']:
            continue
        if len(repo['vulnerabilityAlerts']['nodes']) == MAX_FETCHED:
            print('WARNING: You are hitting the max of {} alerts fetched, while you probably have more, and pagination is currently not implemented'.format(MAX_FETCHED), file=sys.stderr)
        print('https://github.com/{}/{}/network/alerts'.format(viewer_results['login'], repo['name']))
        for alert in repo['vulnerabilityAlerts']['nodes']:
            print('- ' + json.dumps(alert))


if __name__ == '__main__':
    main()
