#!/usr/bin/env python
import os, sys, time
from twilio.rest import TwilioRestClient

# USAGE:
#   export $(xargs < .twilio)
#   cat msg.txt | ./send_text_msg_with_twilio.py 00353860307676

def main(argv):
    twilioClient = TwilioRestClient(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
    phone_number = sys.argv[1]
    message = twilioClient.messages.create(body=sys.stdin.read(), from_=os.environ['TWILIO_NUMBER'], to=phone_number)
    while message.status != 'delivered':
        time.sleep(1)
        message = twilioClient.messages.get(message.sid)
        print(message.status, message.date_sent)

if __name__ == '__main__':
    main(sys.argv[1:])
