#!/usr/bin/env python3
# Jeu de piste / code : minimal Flask web-app that redirect known 6-digits codes to URLs
# LIVE INSTANCE: https://chezsoi.org/lucas/code
# USAGE: URL_PER_CODE='{"1337": "https://chezsoi.org/lucas/blog/"}' ./jdp_code.py
# INSTALL: pip install flask

import json, os, sys
from flask import Flask, redirect, request

URL_PER_CODE = json.loads(os.environ.get('URL_PER_CODE', '{}'))
DEBUG = bool(os.environ.get('DEBUG'))
PORT = int(os.environ.get('PORT', '8083'))
BASE_HTML = '''<!DOCTYPE html>
<head>
  <meta charset="utf-8"/>
  <meta content="IE=edge" http-equiv="X-UA-Compatible"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <title>Quel est le code ?</title>
  <style>
  body {{
    max-width: 46rem;
    margin: 2rem auto;
  }}
  body, input {{
    font-family: Courier, monospace;
    font-size: 2rem;
    line-height: 1.4;
    text-align: center;
    padding: 0 1rem;
  }}
  hr {{ max-width: 20rem; }}
  </style>
</head>
<body>{body}
</body>
</html>'''

def log(*args):
   print(*args, file=sys.stderr)

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def root():
    input_type = request.args.get('t', 'n').lower()  # n (number) OR w (word)
    size = int(request.args.get('s', '6'))
    error = ''
    if request.method == 'POST':
        str_code = request.form['code']
        code = sanitize(str_code, input_type, size)
        if code is None:
            log('Non-sane "code" received:', str_code)
            error = f'Le code reçu n\'a pas le bon format : {str_code}'
        else:
            url = URL_PER_CODE.get(code)
            if url:
                return redirect(url)
            if input_type == 'n':
                code = f'{code:>06}'
            error = f'Code incorrect : {code}'
        error += '\n<br><hr>'
    if input_type == 'w':  # word
        input_html = f'<input type="text" name="code" maxlength="{size}" size="{size}" placeholder="ABCDEFGH" required style="text-transform: uppercase"/>'
    else:  # number
        input_html = f'<input type="number" name="code" maxlength="{size}" size="{size}" placeholder="123456789" required/>'
    body = f'''{error}
    <form method="POST">
        <label for="code">Quel est le code ?</label>
        <br><br>
        {input_html}
        <br><br>
        <input type="submit" value="Essayer"/>
    </form>'''
    return BASE_HTML.format(body=body)

def sanitize(code: str, input_type: str, size: int) -> str | None:
    if len(code) > size:
        return None
    if input_type != 'n':
        return code.upper()
    try:
        return code if int(code) >= 0 else None
    except:
        return None

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
