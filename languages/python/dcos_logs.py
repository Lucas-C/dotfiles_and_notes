#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CLI program to retrieve & tail marathon services logs
# Currently only support HTTP basic auth

# INSTALL: pip install --user requests
# USAGE: ./dcos_logs.py --help

from __future__ import print_function
import argparse, json, logging, os
from http.client import HTTPConnection
import requests
# pylint: disable=no-member,import-error
from requests.packages.urllib3.exceptions import InsecureRequestWarning


READ_LENGTH = 65536  # valeur max prise en compte par l'API, probablement car il s'agit du max pour un unsigned short


def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    args = parse_args()
    username = os.environ.get('DCOS_USERNAME') or input('$DCOS_USERNAME not found, please provide it: ')
    password = os.environ.get('DCOS_PASSWORD') or input('$DCOS_PASSWORD not found, please provide it: ')
    auth = (username, password)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        HTTPConnection.debuglevel = 2

    slave_id, task_id = retrieve_slave_and_task_ids(args, auth)
    files = get_files_list(args, auth, slave_id, task_id)
    if args.list:
        print('/agent/{slave_id}/files/browse:', json.dumps(files, indent=2))
        return

    target_file = next(file for file in files if file['path'].endswith('/' + args.filename))
    offset = 0 if args.whole_file else max(0, target_file['size'] - READ_LENGTH)
    content = get_file_content(args, auth, slave_id, task_id, offset)
    if args.whole_file:
        chunk_size = len(content)
        while True:
            content += get_file_content(args, auth, slave_id, task_id, len(content))
            if len(content) % chunk_size != 0:
                break
    print(content)

    if args.tail:
        offset += len(content)
        while True:
            new_content = get_file_content(args, auth, slave_id, task_id, offset)
            if new_content:
                print(new_content)
                offset += len(new_content)

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--debug', action='store_true', help=' ')
    parser.add_argument('--endpoint-url', required=True, help=' ')
    parser.add_argument('--framework-id', required=True, help='cf. https://mesosphere.github.io/marathon/docs/framework-id.html')
    parser.add_argument('--filename', default='stderr', help=' ')
    parser.add_argument('--whole-file', action='store_true', help='If file length is > {0}b, it will be truncated to only the last {0}b. This will call the API iteratively to retrieve it from offset 0'.format(READ_LENGTH))
    parser.add_argument('--list', action='store_true', help='Only display a list of the remote log files available')
    parser.add_argument('--tail', action='store_true', help='')
    parser.add_argument('app_id', help='Ex: /labelops/dev')
    return parser.parse_args()

def retrieve_slave_and_task_ids(args, auth):
    # Marathon API doc: http://mesosphere.github.io/marathon/api-console/index.html
    response = requests.get('{}/service/marathon/v2/groups'.format(args.endpoint_url),
                            auth=auth, verify=False,
                            params={'embed': ['group.groups', 'group.apps', 'group.apps.tasks']})
    response.raise_for_status()
    target_app = next(app for group in response.json()['groups'] for app in group['apps'] if app['id'] == args.app_id)
    if len(target_app['tasks']) != 1:
        raise NotImplementedError('Zero or several tasks for this app')
    return target_app['tasks'][0]['slaveId'], target_app['tasks'][0]['id']

# pylint: disable=possibly-unused-variable,unused-argument
def get_files_list(args, auth, slave_id, task_id):
    # MESOS API doc: http://mesos.apache.org/documentation/latest/sandbox/#via-the-files-endpoint
    container_id = 'latest'
    response = requests.get('{}/agent/{}/files/browse'.format(args.endpoint_url, slave_id),
                            auth=auth, verify=False,
                            params={'path': '/var/lib/mesos/slave/slaves/{slave_id}/frameworks/{args.framework_id}/executors/{task_id}/runs/{container_id}'.format(**locals())})
    response.raise_for_status()
    files = response.json()
    return files

def get_file_content(args, auth, slave_id, task_id, offset):
    # MESOS API doc: http://mesos.apache.org/documentation/latest/sandbox/#via-the-files-endpoint
    container_id = 'latest'
    response = requests.get('{}/agent/{}/files/read'.format(args.endpoint_url, slave_id),
                            auth=auth, verify=False,
                            params={
                                'path': '/var/lib/mesos/slave/slaves/{slave_id}/frameworks/{args.framework_id}/executors/{task_id}/runs/{container_id}/{args.filename}'.format(**locals()),
                                'length': READ_LENGTH,
                                'offset': offset,
                            })
    response.raise_for_status()
    return response.json()['data']


if __name__ == '__main__':
    main()
