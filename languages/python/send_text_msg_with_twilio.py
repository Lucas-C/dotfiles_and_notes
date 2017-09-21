#!/usr/bin/env python
import os, sys, time
from twilio.rest import Client

# USAGE:
#   export $(xargs < .twilio)
#   curl -u $TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN -G https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/IncomingPhoneNumbers.json | jq -r '.incoming_phone_numbers[].phone_number'
#   cat msg.txt | ./send_text_msg_with_twilio.py 00353860307676

# Interesting twilio widget: https://www.twilio.com/labs/twimlets/menu
# Alt: bandwidth, nexmo, plivo, sinch

def main(argv):
    client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
    src_phone_number = client.incoming_phone_numbers.list()[0].phone_number
    print('src_phone_number=', src_phone_number)
    if len(sys.argv) < 2:
        print('Missing destination number arg. 1st Twilio source number available: {}'.format(src_phone_number))
        return
    dst_phone_number = sys.argv[1]
    message = client.messages.create(body=sys.stdin.read(), from_=src_phone_number, to=dst_phone_number)
    while message.status != 'delivered':
        time.sleep(1)
        message = client.messages.get(message.sid).fetch()
        print(message.status, message.date_sent)

if __name__ == '__main__':
    main(sys.argv[1:])
