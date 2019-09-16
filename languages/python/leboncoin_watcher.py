#!/usr/bin/env python3

# USAGE:
#  export PYTHONPATH=/opt/weboob/modules:~/lucasc_dotfiles_and_notes/languages/python
#  ./leboncoin_watcher.py [--alert-cmd $CMD] [--alert-phone-number $NB] [--debug] < cities.txt

# This script relies on https://github.com/laurentb/weboob/tree/master/modules
# and https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/send_text_msg_with_twilio.py for alerting through SMS.
# Its state is stored as a list of URLs in a leboncoin.json in the current directory.
# Example input file formatting:
#   Trélazé (49800)
#   Angers (toute la ville)

import argparse, json, logging, os, sys
from subprocess import check_output
from weboob.capabilities.housing import City, Query, HOUSE_TYPES, POSTS_TYPES
from leboncoin.browser import LeboncoinBrowser


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug')
    parser.add_argument('--alert-cmd', help='CLI command that takes a message as 1st argument')
    parser.add_argument('--alert-phone-number', help='Will use Twilio API, require $TWILIO_ACCOUNT_SID & $TWILIO_AUTH_TOKEN en vars')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    query_for_cities(parser.parse_args())


def query_for_cities(args):
    cities = [city(line.strip()) for line in args.infile]

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        for handler in logging.root.handlers:
            handler.setLevel(logging.DEBUG)

    with open('leboncoin.json') as json_file:
        prev_urls = json.load(json_file)

    browser = LeboncoinBrowser()
    query = Query()
    # TODO: as an improvment those values could be provided as CLI args:
    query.type = POSTS_TYPES.RENT
    query.house_types = [HOUSE_TYPES.APART, HOUSE_TYPES.HOUSE]
    query.cost_max = 800
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
