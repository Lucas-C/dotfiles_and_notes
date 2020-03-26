#!/usr/bin/env python3
# coding: utf-8
# LIVE INSTANCE: https://chezsoi.org/lucas/jdr/rpg-dice
# INSTALL:
#   pew new rpg-dice -p python3
#   pip install flask
# cat /etc/systemd/system/rpg-dice.service
#   [Service]
#   WorkingDirectory=/path/to/parent/dir
#   ExecStart=/usr/local/bin/pew in rpg-dice python -u rpg_dice.py
# nginx configuration:
#   location /lucas/jdr/rpg-dice {
#       include uwsgi_params;
#       rewrite ^/lucas/jdr/rpg-dice/?(.*)$ /$1 break;
#       proxy_pass http://127.0.0.1:8084;
#   }

import os
from datetime import datetime
from random import randrange
from flask import Flask, request

BASE_URL = os.environ.get('BASE_URL', 'https://chezsoi.org/lucas/jdr/rpg-dice')
BASE_HTML = '''<!DOCTYPE html>
<head>
  <meta charset="utf-8"/>
  <meta content="IE=edge" http-equiv="X-UA-Compatible"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  {meta}
  <title>rpg-dice</title>
  <style>
  body {{
    max-width: 46rem;
    margin: 0 auto;
    font-family: Calibri,Arial,sans-serif;
    font-size: 2rem;
    line-height: 1.4;
    text-align: center;
  }}
  img {{
    display: block;
    margin: 0 auto;
  }}
  body > a {{
    display: block;
    text-decoration: none;
    margin: 5rem auto;
    width: 16rem;
    background: aliceblue;
    border-radius: 1rem;
    padding: 2rem 0;
  }}
  label, input {{
    font-size: 2rem;
    display: block;
    margin: 1rem auto;
  }}
  s {{ /* dices */
    text-decoration: none;
    font-size: 4rem;
    line-height: .8;
    vertical-align: bottom;
  }}
  footer {{ font-size: 1.5rem; }}
  </style>
</head>
<body>
  <h1>rpg-dice</h1>
  <img alt="A pair of dice" src="https://chezsoi.org/lucas/blog/images/jdr/dice.png">
  {body}
  <footer>Source code: <a href="https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/rpg_dice.py">rpg_dice.py</a></footer>
</body>
</html>'''
DIE_ROLLS_PER_ROOM = {}

app = Flask(__name__)

@app.route('/<room>', methods=('GET', 'POST'))
def room(room):
    die_rolls = DIE_ROLLS_PER_ROOM.setdefault(room, [])
    name = ''
    if request.method == 'POST':
        name = request.form['name']
        die = 1 + randrange(6)
        hour = datetime.now().strftime('%X')
        die_rolls.append((name, die, hour))
    html_die_rolls = '\n'.join(to_html(die_roll) for die_roll in reversed(die_rolls))
    return BASE_HTML.format(
        meta=f'<meta http-equiv="refresh" content="3; URL={BASE_URL}/{room}">',
        body='''
        <form onsubmit="return this.name.value.length >= 3" method="POST">
          <label for="name">Name:</label>
          <input type="text" minlength="3" name="name">
          <input type="submit" value="Roll the die">
        </form>
        <ul>{html_die_rolls}</ul>
        <script>
        const nameAlreadyTyped = '{name}';
        if (nameAlreadyTyped) document.forms[0].name.value = nameAlreadyTyped;
        </script>'''.format(**locals()))

@app.route('/')
def homepage():
    return BASE_HTML.format(meta='', body='''
        <a>Create room</a>
        <script>
        const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
        let room = '';
        while (room.length < 6) { room += CHARS[Math.floor(Math.random() * CHARS.length)]; }
        document.getElementsByTagName('a')[0].href = room;
        </script>''')

def to_html(die_roll):
   player, die, hour = die_roll
   emoji = emojify(die)
   return '<li>{player}: <s>{emoji}</s> ({hour})</li>'.format(**locals())

def emojify(die):
    return {1: '⚀', 2: '⚁', 3: '⚂', 4: '⚃', 5: '⚄', 6: '⚅'}[die]


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', '8084')))
