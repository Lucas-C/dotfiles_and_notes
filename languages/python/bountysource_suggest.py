#!/usr/bin/python3

# This script will search for bounties in all GitHub repositories you have already contributed to

# USAGE: GITHUB_TOKEN=... GITHUB_USER=... ./bounty_suggest.py
# (the GITHUB_TOKEN does not need an specific permission, and is optionnal but will help to avoid "API rate limit exceeded" errors)
# REQUIRES: pip install --user pygithub requests

import os
from bs4 import BeautifulSoup
import requests
from github import Github

def extract_html_table(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    if not soup.table:
        return []
    headers = [th['property'] for th in soup.table.find_all('sort-header')]
    rows = []
    for tr in soup.table.find_all('tr')[1:]:
        row = [{'text': tr.get_text().strip(), 'url': tr.a['href'] if tr.a else None} for tr in tr.find_all('td')]
        rows.append({headers[i]: row[i] for i in range(len(row))})
    return rows

gh = Github(os.environ.get('GITHUB_TOKEN'))
print('### Retrieving GitHub PRs created by user:', os.environ['GITHUB_USER'])
user_prs = gh.search_issues('', author=os.environ['GITHUB_USER'], type='pr')  # returns a lazy-requesting generator
user_contributed_repos = set(pr.raw_data['repository_url'].split('/')[-1] for pr in user_prs)
for repo_name in user_contributed_repos:
    print()
    print()
    print('### Searching bountysource.com for issues related to repo:', repo_name)
    print()
    response = requests.get('https://api.bountysource.com/search/bounty_search',
                            params={'page': 1, 'per_page': 250, 'search': repo_name},
                            headers={'Accept': 'application/vnd.bountysource+json; version=1'})
    response.raise_for_status()
    for bounty in response.json()['issues']:
        if not bounty['url'].startswith('https://github.com/{}'.format(repo_name)):  # ignoring false positives
            continue
        print('Title: {}'.format(bounty['title']))
        print('Issue URL: https://www.bountysource.com/{}'.format(bounty['frontend_path']))
        print('BountySource URL: {}'.format(bounty['url']))
        print('Bounty: {}$'.format(int(bounty['bounty_total'])))
        print()

    print()
    print()
    print('### Searching freedomsponsors.org for issues related to repo:', repo_name)
    print()
    response = requests.get('https://freedomsponsors.org/search/', params={'s': repo_name})
    response.raise_for_status()
    matchs = extract_html_table(response.text)
    for match in matchs:
        if match['project']['text'].lower() != repo_name:  # ignoring false positives
            continue
        print('Title: {}'.format(match['title']['text']))
        print('FreedomSponsors URL: https://freedomsponsors.org{}'.format(match['title']['url']))
        bounty = match['offers']['text']
        print('Bounty: {} {}'.format(bounty[:3].strip(), bounty[3:].strip()))
        print()

    # Also: http://www.coderbounty.com
