#!/usr/bin/python

# USAGE:
#   export GITHUB_OAUTH_TOKEN=...
#   ./github_graphql_get_reposecurityvulnerabilities.py

import json, requests

API_KEY = "YOUR_API_KEY"
variables = {"number_of_repos": 100, "number_of_vulns": 100}

graphql_query = '''query($number_of_repos:Int!, $number_of_vulns:Int!, $next_cursor:String) {
  organization(login: "gelatoas") {
repositories(first: $number_of_repos after:$next_cursor) {
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
      nodes {
        createdAt
        vulnerableRequirements
        dismissedAt
        dismissReason
        securityVulnerability {
          advisory {
            description
            identifiers 
              { 
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


def getResults(variables):
    response = requests.post('https://api.github.com/graphql',
                             data=json.dumps({'query': graphql_query, 'variables': variables}),
                             headers={'Authorization': 'bearer ' + API_KEY,
                                      # cf. https://developer.github.com/v4/guides/forming-calls/#authenticating-with
                                      # -graphql
                                      'Accept': 'application/vnd.github.vixen-preview+json'})  # cf.
    # https://developer.github.com/v4/previews/#repository-vulnerability-alerts
    response.raise_for_status()
    #print(response.text)
    viewer_results = response.json()['data']['organization']

    return viewer_results


def printResults(result):
    for repo in result['repositories']['nodes']:
        if not repo['vulnerabilityAlerts']['nodes']:
            continue
        #print('https://github.com/{}/{}/network/alerts'.format("gelatoas", repo['name']))
        results_json = {"repo": {"name": repo['name']}}
        for alert in repo['vulnerabilityAlerts']['nodes']:
            results_json.update(alert)
            print(json.dumps(results_json))


def main():
    result = getResults(variables)
    while result['repositories']['pageInfo']['hasNextPage'] == True:
        printResults(result)
        nextCursor = result['repositories']['pageInfo']['endCursor']
        variables.update({"next_cursor": nextCursor})
        result = getResults(variables)


if __name__ == '__main__':
    main()
