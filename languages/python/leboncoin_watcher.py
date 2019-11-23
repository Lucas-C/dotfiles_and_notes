#!/usr/bin/env python3

# USAGE:
#  export PYTHONPATH=/opt/weboob/modules:~/lucasc_dotfiles_and_notes/languages/python
#  ./leboncoin_watcher.py --type RENT [--cost-max 800] [--alert-cmd $CMD] [--alert-phone-number $NB] [--debug] cities.txt

# This script relies on the weboob Pypi package, and https://github.com/laurentb/weboob/tree/master/modules/leboncoin
# and https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/send_text_msg_with_twilio.py for alerting through SMS.
# Its state is stored as a list of URLs in a leboncoin.json in the current directory.
# Example of input file format:
#   Trélazé (49800)
#   Angers (toute la ville)

import argparse, json, logging, os, random, sys
from subprocess import check_output

from weboob.capabilities.housing import City, Query, HOUSE_TYPES, POSTS_TYPES
from leboncoin.browser import LeboncoinBrowser
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def main(argv=None):
    query_for_cities(parse_args(argv))

def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--type', choices=list(POSTS_TYPES._keys), required=True)
    parser.add_argument('--house-types', choices=list(HOUSE_TYPES._keys), nargs='+', default=['APART', 'HOUSE'])
    parser.add_argument('--area-min', type=int)
    parser.add_argument('--area-max', type=int)
    parser.add_argument('--cost-min', type=int)
    parser.add_argument('--cost-max', type=int)
    parser.add_argument('--nb-rooms', type=int)
    parser.add_argument('--alert-cmd', help='CLI command that takes a message as 1st argument')
    parser.add_argument('--alert-phone-number', help='Will use Twilio API, require $TWILIO_ACCOUNT_SID & $TWILIO_AUTH_TOKEN en vars')
    parser.add_argument('--proxies', type=argparse.FileType('r'))
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    return parser.parse_args(argv)

def query_for_cities(args):
    cities = [city(line.strip()) for line in args.infile]

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        for handler in logging.root.handlers:
            handler.setLevel(logging.DEBUG)

    try:
        with open('leboncoin.json') as json_file:
            prev_urls = json.load(json_file)
    except FileNotFoundError:
        prev_urls = []

    proxy = None
    if args.proxies:
        proxy = {'https': random.choice(list(args.proxies)).strip()}
        LeboncoinBrowser.VERIFY = False
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    browser = LeboncoinBrowser(proxy=proxy)
    query = Query()
    query.type = POSTS_TYPES[args.type]
    query.house_types = [HOUSE_TYPES[ht] for ht in args.house_types]
    if query.area_min:
        query.area_min = args.area_min
    if query.area_max:
        query.area_max = args.area_max
    if query.cost_min:
        query.cost_min = args.cost_min
    if query.cost_max:
        query.cost_max = args.cost_max
    if query.nb_rooms:
        query.nb_rooms = args.nb_rooms
    new_urls = []
    for i in range(0, len(cities), 10):  # if the frontend tells the truth, the API supports max 10 cities at a time
        query.cities = cities[i:i+10]
        for housing in browser.search_housings(query, None):
            new_urls.append(housing.url)

    diff_urls = r'\n'.join(set(new_urls) - set(prev_urls))

    print('Saving {} current housing matches to leboncoin.json'.format(len(new_urls)))
    with open('leboncoin.json', 'w+') as json_file:
        json.dump(new_urls, json_file)

    print(diff_urls.replace(r'\n', '\n'))
    if diff_urls:
        msg = r'Nouvelle(s) annonce(s) LeBonCoin:\n' + diff_urls
        if args.alert_cmd:
            check_output([args.alert_cmd, msg])
        if args.alert_phone_number:
            from send_text_msg_with_twilio import send_text_msg
            send_text_msg(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'], args.alert_phone_number, msg)

def city(label):
    'cf. https://github.com/laurentb/weboob/blob/master/modules/leboncoin/browser.py#L113'
    c = City()
    c.name = label
    if 'toute la ville' in label:
        c.id = label.split(' ')[0] + ' '
    else:
        c.id = label.replace('(', '').replace(')', '')
    return c


if __name__ == '__main__':
    main()
