#!/usr/bin/env python3
# Basic script to demonstrate connexion to the HTTP API of a Jenkins server, even without admin permissions.
# INSTALL: pip install jenkinsapi
# USAGE:
#   export COOKIE=JSESSIONID.abcdef1234=node0123456789abcdef.node0
#   ./jenkins_api.py $JENKINS_URL
import logging, os, sys
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.requester import Requester


def main():
    jenkins_url = sys.argv[1]

    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s')
    # Don't need to hear about connections being opened / closed:
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    # Allow to follow folder traversal progress:
    logging.getLogger('jenkinsapi.jenkinsbase').setLevel(logging.DEBUG)
    # Ease the debug of HTTP errors in block_until_complete:
    logging.getLogger('jenkinsapi.queue').setLevel(logging.DEBUG)

    if os.environ.get('COOKIE'):
        print('Using cookie-based auth')
        jenkins = Jenkins(jenkins_url, timeout=20, lazy=True)
        Requester.AUTH_COOKIE = os.environ['COOKIE']
    else:
        print(f'Using user token-based auth ( can be generated from {jenkins_url}/me/configure )')
        jenkins = Jenkins(jenkins_url, timeout=20, lazy=True, username=os.environ['USERNAME'], password=os.environ['TOKEN'])

    print('jenkins.version=', jenkins.version)

    print('Listing agent nodes:')
    for node in jenkins.nodes.values():  # requests $JENKINS_URL/computer/api/json
        # All Node available methods: https://github.com/pycontribs/jenkinsapi/blob/master/jenkinsapi/node.py#L201
        print(f'- {node}: num_executors={node.get_num_executors()} online={node.is_online()} {node.offline_reason()}')
        print(f'  labels: {" ".join(l["name"] for l in node._data["assignedLabels"])}')

    print('Now trying to list plugins (admin permissions required):')
    for plugin in jenkins.plugins.values():  # requests $JENKINS_URL/pluginManager/api/json?depth=1
        print(f'- Short Name: {plugin.shortName}')
        print(f'  Long Name: {plugin.longName}')
        print(f'  Version: {plugin.version}')
        print(f'  URL: {plugin.url}')
        print(f'  Active: {plugin.active}')
        print(f'  Enabled: {plugin.enabled}')


if __name__ == '__main__':
    main()
