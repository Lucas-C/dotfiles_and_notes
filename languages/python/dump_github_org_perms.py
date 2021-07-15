#!/usr/bin/python

# If descriptor file already exist, log every change: add / rm / value modification

# USAGE:
#   export GITHUB_API_TOKEN=...
#   ./dump_github_org_perms.py github_perms.yaml --new-org voyages-sncf-technologies --ignore-403s

from __future__ import print_function
import argparse, os, sys
from datetime import datetime

from agithub.GitHub import GitHub
from agithub.base import IncompleteRequest
import yaml
try:
    from colorama import Fore, init  # optionnal dependency
    init()  # for Windows
except ImportError:  # fallback so that the imported classes always exist
    class ColorFallback():
        __getattr__ = lambda self, name: ''
    Fore = ColorFallback()


def main():
    if 'GITHUB_API_TOKEN' not in os.environ:
        raise RuntimeError('Environment variable GITHUB_API_TOKEN must be defined')
    args = parse_args()
    descriptor = {}
    if os.path.exists(args.descriptor_filepath):
        with open(args.descriptor_filepath) as descriptor_file:
            descriptor = yaml.safe_load(descriptor_file) or {}
    ag = GitHubAPIWrapper(token=os.environ['GITHUB_API_TOKEN'], ignore_403s=args.ignore_403s)
    descriptor = update_descriptor_from_github(descriptor, ag, args.new_org)
    if args.check_logins_with_activedirectory:
        check_logins_with_activedirectory(descriptor['members'])
    if args.dry_run:
        yaml.dump_all([descriptor], sys.stdout, default_flow_style=False, Dumper=NoAliasSafeDumper)
    else:
        with open(args.descriptor_filepath, 'w') as descriptor_file:
            yaml.dump_all([descriptor], descriptor_file, default_flow_style=False, Dumper=NoAliasSafeDumper)


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    parser.add_argument('descriptor_filepath', help='YAML file')
    parser.add_argument('--new-org', help=' ')
    parser.add_argument('--dry-run', action='store_true', help=' ')
    parser.add_argument('--ignore-403s', action='store_true', help=' ')
    args = parser.parse_args()
    if not args.github_to_descriptor and not args.github_from_descriptor:
        parser.error('You must choose one of --github-to-descriptor / --github-from-descriptor')
    if args.github_to_descriptor and args.github_from_descriptor:
        parser.error('You must choose only one of --github-to-descriptor / --github-from-descriptor')
    return args


def update_descriptor_from_github(descriptor, ag, new_org_name=None):
    org = descriptor.setdefault('org', new_org_name)
    if not org:
        raise RuntimeError('An "org" field must be present in your YAML, or you must provide the --new-org arg')

    # Updating org members
    members_desc = descriptor.setdefault('members', {})  # type: Dict[str, str]
    gh_members = ag.orgs[org].members.get()  # type: List[str]
    descriptor_list_add_rm('.members', members_desc, gh_members, field='login')

    # Updating org repos
    repos_desc = descriptor.setdefault('repos', {})
    gh_repos = ag.orgs[org].repos.get()
    descriptor_dict_add_rm('.repos', repos_desc, gh_repos, key_field='name', value_field={})
    for repo_name, repo_desc in repos_desc.items():
        collabs_desc = repo_desc.setdefault('collaborators', {})
        gh_collabs = ag.repos[org][repo_name].collaborators.get(affiliation='direct')
        for collab_login in set(collabs_desc.keys()) & set(c['login'] for c in gh_collabs):
            gh_collab = next(c for c in gh_collabs if c['login'] == collab_login)
            descriptor_value_update('.repos.collaborators'.format(collab_login), collabs_desc, collab_login, gh_collab['permissions'])
        descriptor_dict_add_rm('.repos.collaborators', collabs_desc, gh_collabs, key_field='login', value_field='permissions')

        teams_desc = repo_desc.setdefault('teams', {})
        gh_teams = ag.repos[org][repo_name].teams.get()
        for team_name in set(teams_desc.keys()) & set(t['name'] for t in gh_teams):
            gh_team = next(t for t in gh_teams if t['name'] == team_name)
            descriptor_value_update('.repos.teams'.format(team_name), teams_desc, team_name, gh_team['permission'])
        descriptor_dict_add_rm('.repos.teams', teams_desc, gh_teams, key_field='name', value_field='permission')

    # Updating org teams
    teams_desc = descriptor.setdefault('teams', {})
    gh_teams = ag.orgs[org].teams.get()
    descriptor_dict_add_rm('.teams', teams_desc, gh_teams, key_field='id', value_field={})
    for team_id in set(teams_desc.keys()) & set(t['id'] for t in gh_teams):
        team_desc = teams_desc.setdefault(team_id, {})
        gh_team = next(t for t in gh_teams if t['id'] == team_id)
        descriptor_value_update('.teams[{}].name'.format(team_id), team_desc, 'name', gh_team['name'])
        descriptor_value_update('.teams[{}].privacy'.format(team_id), team_desc, 'privacy', gh_team['privacy'])
        descriptor_value_update('.teams[{}].permission'.format(team_id), team_desc, 'permission', gh_team['permission'])
        team_members_desc = team_desc.setdefault('members', [])
        gh_team_members = ag.teams[gh_team['id']].members.get()
        descriptor_list_add_rm('.teams[{}].members'.format(team_id), team_members_desc, gh_team_members, field='login')

    descriptor['last_update_date'] = datetime.utcnow().isoformat()
    return descriptor


def descriptor_value_update(path, node, field, new_value):
    if field in node and node[field] != new_value:
        log('{} CHANGED: {} -> {}'.format(path, node[field], new_value), log_type='change')
    node[field] = new_value


def descriptor_list_add_rm(path, items_list, new_items, field):
    new_items = [i[field] for i in new_items]
    for new_item in set(new_items) - set(items_list):
        log('{} ADDED: {}'.format(path, new_item), log_type='add')
        items_list.append(new_item)
    for rm_item in set(items_list) - set(new_items):
        log('{} REMOVED: {}'.format(path, rm_item), log_type='rm')
        items_list.remove(rm_item)


def descriptor_dict_add_rm(path, items_dict, new_items, key_field, value_field=True, log_old_value=False):
    new_items_dict = {item[key_field]: item for item in new_items}
    for new_item_key in set(new_items_dict.keys()) - set(items_dict.keys()):
        log('{} ADDED: {}'.format(path, new_item_key), log_type='add')
        value = new_items_dict[new_item_key] if value_field is True else (new_items_dict[new_item_key][value_field] if isinstance(value_field, str) else value_field)
        items_dict[new_item_key] = value
    for rm_item_key in set(items_dict.keys()) - set(new_items_dict.keys()):
        suffix = ' - {}'.format(items_dict[rm_item_key]) if log_old_value else ''
        log('{} REMOVED: {}{}'.format(path, rm_item_key, suffix), log_type='rm')
        del items_dict[rm_item_key]


def log(msg, log_type):
    if not log_type:
        return print(msg)
    color_start = {
        'rm': Fore.RED,
        'add': Fore.GREEN,
        'change': Fore.CYAN,
    }[log_type]
    print('{}{}{}'.format(color_start, msg, Fore.RESET))


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
        if http_code == 404:
            return []
        if http_code == 403 and self.ignore_403s:
            print('HTTP {}: {}'.format(http_code, response['message']), file=sys.stderr)
            return []
        if http_code != 200:
            raise RuntimeError('HTTP code: {}: {}'.format(http_code, response))
        return response


class NoAliasSafeDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


if __name__ == '__main__':
    main()
