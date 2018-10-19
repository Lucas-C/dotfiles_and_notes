#!/usr/bin/python

# USAGE:
#   export GITHUB_OAUTH_TOKEN=...
#   ./github_graphql_get_reposecurityvulnerabilities.py

import json, os, requests


def main():
    graphql_query = 'query { viewer { login repositories(isFork: false, first: 100) { nodes { name vulnerabilityAlerts(first: 100) { nodes { packageName affectedRange externalReference fixedIn } } } } } }'
    oauth_token = os.environ['GITHUB_OAUTH_TOKEN']  # cf. https://developer.github.com/v4/guides/forming-calls/#authenticating-with-graphql
    response = requests.post('https://api.github.com/graphql',
                             data=json.dumps({'query': graphql_query}),
                             headers={'Authorization': 'bearer ' + oauth_token,
                                      'Accept': 'application/vnd.github.vixen-preview+json'})  # cf. https://developer.github.com/v4/previews/#repository-vulnerability-alerts
    response.raise_for_status()
    login = response.json()['data']['viewer']['login']
    for repo in response.json()['data']['viewer']['repositories']['nodes']:
        if repo['vulnerabilityAlerts']['nodes']:
            print('https://github.com/{}/{}/network/alerts'.format(login, repo['name']))
            for alert in repo['vulnerabilityAlerts']['nodes']:
                print('- ' + json.dumps(alert))


if __name__ == '__main__':
    main()
