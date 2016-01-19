#!/usr/bin/python2
# Original idea: http://sametmax.com/floodsport
# Max gmail subject width on my display: 74

import aalib
import Image
from itertools import repeat
from getpass import getpass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

image_name = 'i_love_heart_laetitia.jpg'
height = 40
width = 70
servername = 'smtp.gmail.com:587'

def send_emails(from_user, to_user, username, password, servername, subject_altext_html_contents):
    server = smtplib.SMTP()
    server.connect(servername)
    server.starttls()
    server.login(username, password)
    for subject, alttext, html_body in subject_html_text_contents:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg.attach(MIMEText(alttext, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        server.sendmail(from_user, to_user, msg.as_string())
    server.quit()

def ascii_lines_generator(image_name, height, width):
    screen = aalib.AsciiScreen(width=width, height=height)
    image = Image.open(image_name).convert('L').resize(screen.virtual_size)
    screen.put_image((0, 0), image)
    for line in screen.render().split('\n'):
        yield line

def monospace_html(text):
    return "<pre>{}</pre>".format(text)

username = sys.argv[1]
username = '{}@gmail.com'.format(username)
print username
password = getpass()
from_user = username # Gmail check ?
to_user = sys.argv[2] if len(sys.argv) > 2 else username

lines = ascii_lines_generator(image_name, height, width)
subjects = repeat('Do you read me ?')
text_bodies = repeat('Alt text')
html_bodies = (monospace_html("\n".join(lines)),)
contents = zip(subjects, text_bodies, html_bodies)
send_emails(from_user, to_user, username, password, servername, contents)

