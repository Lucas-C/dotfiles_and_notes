# -*- coding: utf-8 -*-

from getpass import getpass
import smtplib
from email.MIMEText import MIMEText
import sys

username = sys.argv[1]
username = '{}@gmail.com'.format(username)
print username
password = getpass()

message = MIMEText('You like my body ?')
message['Subject'] = '123456789A123456789B123456789C123456789D123456789E123456789F123456789G123456789H' # max width: 74

server = smtplib.SMTP()
server.connect('smtp.gmail.com', '587')
server.ehlo()
server.starttls()
server.login(username, password)
server.sendmail(username, username, message.as_string())
server.quit()
