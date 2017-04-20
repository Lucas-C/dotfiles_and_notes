#!/usr/bin/env python
from Skype4Py import Skype
import sys

# USAGE:
#   skype
#   cat msg.txt | ./send_text_msg_with_skype.py 00353860307676
#   (then authorize skype4py in Skype client popup)

def main(argv):
    client = Skype()
    client.Attach()
    phone_number = sys.argv[1]
    client.SendSms(phone_number, Body=sys.stdin.read())

if __name__ == '__main__':
    main(sys.argv[1:])
