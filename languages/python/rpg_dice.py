#!/usr/bin/env python3
# coding: utf-8
# LIVE INSTANCE: https://chezsoi.org/lucas/jdr/rpg-dice
# USAGE: ./rpg_dice.py
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
from collections import OrderedDict
from datetime import datetime
from random import randrange
from flask import Flask, jsonify, request

BASE_URL = os.environ.get('BASE_URL', 'https://chezsoi.org/lucas/jdr/rpg-dice')
BASE_HTML = '''<!DOCTYPE html>
<head>
  <meta charset="utf-8"/>
  <meta content="IE=edge" http-equiv="X-UA-Compatible"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
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
    max-width: 15rem;
  }}
  figcaption {{ font-size: .8rem; }}
  body > a {{
    display: block;
    text-decoration: none;
    margin: 3rem auto;
    width: 16rem;
    background: aliceblue;
    border-radius: 1rem;
    padding: 2rem 0;
  }}
  button, label, input {{
    font-size: 2rem;
    display: block;
    margin: 1rem auto;
    max-width: 15rem;
  }}
  input[type="number"] {{ width: 4rem; }}
  p {{ font-size: 1.5rem; }}
  s {{ /* dices */
    text-decoration: none;
    font-size: 4rem;
    line-height: .8;
    vertical-align: bottom;
  }}
  footer {{ font-size: 1.5rem; }}
  #timer {{
    font-size: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    max-width: 20rem;
    margin: 0 auto;
  }}
  </style>
</head>
<body>
  <h1>rpg-dice</h1>
  <figure>
    <img alt="A pair of dice" src="https://chezsoi.org/lucas/jdr/dice.png">
    <figcaption><a href="https://www.deviantart.com/durpy/art/Cutie-Mark-Dice-294117495">Cutie Mark - Dice by Durpy</a> - CC BY-NC 3.0</figcaption>
  </figure>
  {body}
  <footer>Source code: <a href="https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/rpg_dice.py">rpg_dice.py</a></footer>
</body>
</html>'''
DIE_ROLLS_PER_TABLE = OrderedDict()  # in-memory data state
MAX_TABLES_COUNT = 50

app = Flask(__name__)

@app.route('/<table>', methods=('GET', 'POST'))
def table_html(table):
    die_rolls = DIE_ROLLS_PER_TABLE.setdefault(table, [])
    name = ''
    if request.method == 'POST':
        autocleanup()
        name = request.form['name']
        die = 1 + randrange(6)
        hour = datetime.now().strftime('%X')
        die_rolls.append((name, die, hour))
    json_endpoint = f'{BASE_URL}/{table}/json'
    return BASE_HTML.format(
        body='''
        <div id="timer" style="visibility: hidden">
          <button onclick="startTimer(this)">Start timer</button>
          <input type="number" value="20"></input>min
        </div>
        <form onsubmit="return this.name.value.length >= 3" method="POST">
          <label for="name">Name:</label>
          <input type="text" minlength="3" name="name">
          <input type="submit" value="Roll the die">
        </form>
        <p>The die rolls of all people using this URL are displayed below :</p>
        <ul id="rolls"></ul>
        <script>
        const nameAlreadyTyped = '{name}';
        const queryParams = new URLSearchParams(location.search);
        if (queryParams.get('timer')) {{
          document.getElementById('timer').style.visibility = 'visible';
        }}
        if (nameAlreadyTyped) document.forms[0].name.value = nameAlreadyTyped;
        window.dieRolls = [];
        function startTimer(button) {{
          chrono(button.parentNode, new Date());
          button.nextElementSibling.remove();
          button.remove();
        }}
        function chrono(timerElem, startTime) {{
          let remaingSeconds = 20 * 60 - Math.floor((new Date() - startTime) / 1000);
          timerElem.textContent = `${{Math.floor(remaingSeconds / 60)}}:${{(remaingSeconds % 60 + '').padStart(2, '0')}}`;
          setTimeout(chrono, 1000, timerElem, startTime);
        }}
        function watchForever() {{
          fetch('{json_endpoint}').then(resp => resp.json()).then(dieRolls => {{
            if (dieRolls.length != window.dieRolls.length) {{
              window.dieRolls = dieRolls;
              const ul = document.getElementById('rolls');
              while (ul.firstChild) {{ ul.removeChild(ul.firstChild); }}
              dieRolls.forEach(dieRoll => {{
                const li = document.createElement('li');
                li.innerHTML = `${{dieRoll.player}}: <s>${{dieRoll.dieChar}}</s> (${{dieRoll.hour}})`;
                ul.appendChild(li);
              }});
            }}
            setTimeout(watchForever, 2000);
          }}).catch(error => console.error(error));
        }}
        watchForever();
        </script>'''.format(**locals()))

@app.route('/<table>/json')
def table_json(table):
    die_rolls = DIE_ROLLS_PER_TABLE.setdefault(table, [])
    return jsonify([to_json(die_roll) for die_roll in reversed(die_rolls)])

@app.route('/')
def homepage_html():
    return BASE_HTML.format(body='''
        <a id="enter-table">Create table</a>
        <script>
        const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
        let table = '';
        while (table.length < 6) {{ table += CHARS[Math.floor(Math.random() * CHARS.length)]; }}
        document.getElementById('enter-table').href = '{BASE_URL}/' + table;
        </script>'''.format(BASE_URL=BASE_URL))

def to_json(die_roll):
    player, die, hour = die_roll
    return {
        'player': player,
        'dieChar': emojify(die),
        'hour': hour,
    }

def emojify(die):
    return {1: '⚀', 2: '⚁', 3: '⚂', 4: '⚃', 5: '⚄', 6: '⚅'}[die]

def autocleanup():
    while len(DIE_ROLLS_PER_TABLE) > MAX_TABLES_COUNT:
        table, _ = DIE_ROLLS_PER_TABLE.popitem(last=True)
        print('autocleanup removed table:', table)


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', '8084')))
