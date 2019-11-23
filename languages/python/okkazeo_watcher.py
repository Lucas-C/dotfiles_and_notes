#!/usr/bin/env python3

# Note: les CGV n'interdisent pas ce type de scraping, en date du 2019/11/23
# -> https://www.okkazeo.com/okkazeo/cgv

import argparse, os


from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


USER_AGENT = os.path.join('https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/',
                          os.path.basename(__file__))


def main(argv=None):
    search_for_game_vendors(parse_args(argv))

def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('game_id')
    parser.add_argument('--name', help='Game name to include in alert message')
    parser.add_argument('--department', type=int)
    parser.add_argument('--alert-cmd', help='CLI command that takes a message as 1st argument')
    parser.add_argument('--alert-phone-number', help='Will use Twilio API, require $TWILIO_ACCOUNT_SID & $TWILIO_AUTH_TOKEN en vars')
    return parser.parse_args()

def search_for_game_vendors(args):
    params = None
    if args.department:
        params = {'departement': args.department}
    resp = requests.get('https://www.okkazeo.com/jeux/view/' + args.game_id, params=params,
                        headers = {'User-Agent': USER_AGENT})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find(id='absence_annonce'):
        return
    msg = 'Nouvelle(s) offre(s) Okkazeo pour le jeu '
    msg += args.name if args.name else str(args.game_id)
    if args.department:
        msg += ' dans le departement ' + str(args.department)
    print(msg)
    if args.alert_cmd:
        check_output([args.alert_cmd, msg])
    if args.alert_phone_number:
        from send_text_msg_with_twilio import send_text_msg
        send_text_msg(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'], args.alert_phone_number, msg)

if __name__ == '__main__':
    main()
