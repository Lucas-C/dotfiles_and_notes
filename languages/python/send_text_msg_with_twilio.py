#!/usr/bin/env python
import os, sys, time
from twilio.rest import TwilioRestClient

# USAGE:
#   export $(xargs < .twilio)
#   curl -u $TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN -G https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/IncomingPhoneNumbers.json | jq -r '.incoming_phone_numbers[].phone_number'
#   cat msg.txt | ./send_text_msg_with_twilio.py 00353860307676

# Interesting twilio widget: https://www.twilio.com/labs/twimlets/menu

def main(argv):
    twilioClient = TwilioRestClient(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
    phone_numbers = twilioClient.phone_numbers.list()
    src_phone_number = phone_numbers[0].phone_number
    print('src_phone_number=', src_phone_number)
    if len(sys.argv) < 2:
        print('Missing destination number arg. 1st Twilio source number available: {}'.format(src_phone_number))
        return
    dst_phone_number = sys.argv[1]
    message = twilioClient.messages.create(body=sys.stdin.read(), from_=src_phone_number, to=dst_phone_number)
    while message.status != 'delivered':
        time.sleep(1)
        message = twilioClient.messages.get(message.sid)
        print(message.status, message.date_sent)

if __name__ == '__main__':
    main(sys.argv[1:])
