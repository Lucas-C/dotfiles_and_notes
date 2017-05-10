#!/usr/bin/env python3
import os, sys
from twilio.rest import Client

# USAGE:
#   export $(xargs < .twilio)
#   ./record_voicemail_with_twilio.py

def main(argv):
    client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
    client.calls.create(to='+33241395037',
                        from_=client.incoming_phone_numbers.list()[0].phone_number,
                        record=True,
                        url='https://handler.twilio.com/twiml/EH9515e9e0d2fb81f27d75a493225ae703')
# This Twiml file content:
#<?xml version="1.0" encoding="UTF-8"?>
#<Response>
#    <Pause length="30"/>
#</Response>

if __name__ == '__main__':
    main(sys.argv[1:])
