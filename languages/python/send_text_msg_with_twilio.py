#!/usr/bin/env python
import os, sys, time
from twilio.rest import Client

# USAGE:
#   export $(xargs < .twilio)
#   curl -u $TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN -G https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/IncomingPhoneNumbers.json | jq -r '.incoming_phone_numbers[].phone_number'
#   cat msg.txt | ./send_text_msg_with_twilio.py 00353860307676

# Interesting twilio widget: https://www.twilio.com/labs/twimlets/menu
# Alt: bandwidth, nexmo, plivo, sinch

def main():
    if len(sys.argv) < 2:
        raise ValueError('Missing destination number arg. 1st Twilio source number available: {}'.format(src_phone_number))
    send_text_msg(os.environ['TWILIO_ACCOUNT_SID'],
                  os.environ['TWILIO_AUTH_TOKEN'],
                  sys.argv[1], sys.stdin.read())

def send_text_msg(account_sid, auth_token, dst_phone_number, message)
    client = Client(account_sid, auth_token)
    src_phone_number = client.incoming_phone_numbers.list()[0].phone_number
    print('src_phone_number=', src_phone_number)
    message = client.messages.create(body=message, from_=src_phone_number, to=dst_phone_number)
    while message.status != 'delivered':
        time.sleep(1)
        message = client.messages.get(message.sid).fetch()
        print(message.status, message.date_sent)

if __name__ == '__main__':
    main()
