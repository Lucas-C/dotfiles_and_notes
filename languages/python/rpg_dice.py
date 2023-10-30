#!/usr/bin/env python3
# Zero-config, single-file, Python web-app to perform & share dice rolls
# Features:
# * name your room as you want: just choose a custom URL
# * variable number of d6 can be rolled
# * in-memory data storage, with RAM usage control (no more than 50 tables can exist)
# * optional Blades in the Dark result interpretation with ?bitd=1
# * optional name prefill with ?name=
# * optional timer with ?timer=1

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

import os, sys
from collections import OrderedDict
from datetime import datetime
from random import randrange
from string import ascii_letters, digits
from uuid import uuid4
from flask import Flask, jsonify, make_response, request

DEBUG = bool(os.environ.get('DEBUG'))
PORT = int(os.environ.get('PORT', '8084'))
BASE_URL = f"http://localhost:{PORT}" if DEBUG else (os.environ.get('BASE_URL') or 'https://chezsoi.org/lucas/jdr/rpg-dice')
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
  button, label, input {{ font-size: 2rem; }}
  input[type="text"] {{ max-width: 20rem; text-align: center; }}
  input[type="number"] {{ max-width: 4rem; }}
  button, input[type="submit"] {{
    display: block;
    margin: 1rem auto;
  }}
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
  <footer>Source code: <a href="https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/rpg_dice.py">rpg_dice.py</a> - Backup app: <a href="https://www.rolldicewithfriends.com">RollDiceWithFriends</a></footer>
</body>
</html>'''
DIE_ROLLS_PER_TABLE = OrderedDict()  # in-memory data state
MAX_DICE_ROLLED = 10
MAX_TABLES_COUNT = 50

def log(*args):
   print(*args, file=sys.stderr)

app = Flask(__name__)

@app.route('/<table>', methods=('GET', 'POST'))
def table_html(table):
    die_rolls = DIE_ROLLS_PER_TABLE.setdefault(table, [])
    if request.method == 'POST':
        autocleanup()
        name = request.form['name']
        if not is_sane(name):
            log('Non-sane "name" received:', name)
            return make_response(jsonify({'error': f'Non-sane "name" received: {name}'}), 404)
        dice_count = int(request.form['dice-count'])
        if dice_count > MAX_DICE_ROLLED:
            log('Requested "dice-count" is too high:', dice_count)
            return make_response(jsonify({'error': f'Requested "dice-count" is too high: {dice_count}'}), 404)
        roll_type = None
        if dice_count == 0 and request.args.get('bitd'):
            dice_count = 2
            roll_type = "WORST"
        results = []
        for _ in range(dice_count):
            results.append(1 + randrange(6))
        time = datetime.now()
        die_rolls.append((name, results, time, roll_type))
    else:
        name = request.args.get('name') or ''
    json_endpoint = f'{BASE_URL}/{table}/json'
    nonce = uuid4()
    response = make_response(BASE_HTML.format(
        body='''
        <div id="timer" style="visibility: hidden">
          <button>Start timer</button>
          <input type="number" value="20"></input>min
        </div>
        <form method="POST">
          <label id="name-label" for="name">Name:</label>
          <input type="text" minlength="3" name="name">
          <br>
          <label id="dice-count-label" for="dice-count">#d6:</label>
          <input type="number" name="dice-count" min="0" max="10">
          <input type="submit" value="Roll the die">
        </form>
        <p>The die rolls of all people using this URL are displayed below :</p>
        <ul id="rolls"></ul>
        <script nonce="{nonce}">
        const nameAlreadyTyped = '{name}';
        const queryParams = new URLSearchParams(location.search);
        const isBitD = queryParams.get('bitd');
        if (queryParams.get('timer')) {{
          document.getElementById('timer').style.visibility = 'visible';
        }}
        document.getElementsByName('dice-count')[0].value = queryParams.get('dice-count') || 1;
        if (nameAlreadyTyped) document.forms[0].name.value = nameAlreadyTyped;
        window.dieRolls = [];
        function startTimer(button) {{
          chrono(button.parentNode, new Date());
          button.nextElementSibling.remove();
          button.remove();
        }}
        document.getElementsByTagName('button')[0].onclick = startTimer;
        document.getElementsByTagName('form')[0].onsubmit = function () {{
          return this.name.value.length >= 3;
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
                let html = `${{dieRoll.player}}: <s>${{dieRoll.dieChars}}</s>`;
                if (isBitD) {{
                    html += ` <em>${{dieRoll.bitd}}</em>`;
                }}
                html += ` <small>(${{dieRoll.hour}})</small>`;
                li.innerHTML = html;
                ul.appendChild(li);
              }});
            }}
            setTimeout(watchForever, 2000/*ms*/);
          }}).catch(error => console.error(error));
        }}
        watchForever();
        </script>'''.format(**locals())))
    response.headers['Content-Security-Policy'] = f"script-src 'self' 'nonce-{nonce}'"
    return response

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
    first_second_of_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    player, results, time, roll_type = die_roll
    return {
        'player': player,
        'roll_type': roll_type,
        'dieChars': ' '.join(emojify(die) for die in results),
        'bitd': bitd_result(results, roll_type),
        # It would be cleaner to have this date being formatted by the fronted, but YAGNI:
        'hour': time.strftime('%X') if time > first_second_of_today else time.strftime('%x %X'),
    }

def emojify(die):
    return {1: '⚀', 2: '⚁', 3: '⚂', 4: '⚃', 5: '⚄', 6: '⚅'}[die]

def bitd_result(results, roll_type):
    if roll_type == "WORST":
        results = [min(results)]
    six_count = sum(1 for die in results if die == 6)
    if six_count > 1:
        return "CRITICAL success!"
    if six_count == 1:
        return "full success"
    if max(results or ()) in (4, 5):
        return "partial success"
    return "bad outcome"

def autocleanup():
    while len(DIE_ROLLS_PER_TABLE) > MAX_TABLES_COUNT:
        table, _ = DIE_ROLLS_PER_TABLE.popitem(last=True)
        log('autocleanup removed table:', table)

VALID_CHARS = ascii_letters + digits + '-_.:|=+@#$%'
def is_sane(str):
    return all(c in VALID_CHARS for c in str)

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
