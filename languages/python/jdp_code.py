#!/usr/bin/env python3
# Jeu de piste / code : minimal Flask web-app that redirect known 6-digits codes to URLs
# LIVE INSTANCE: https://chezsoi.org/lucas/code
# USAGE: ./jdp_code.py
# INSTALL: pip install flask

import os, sys
from flask import Flask, redirect, request

URL_PER_CODE = {
    1337: "https://chezsoi.org/lucas/blog/",
}

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
    margin: 0 auto;
  }}
  body, input {{
    font-family: Calibri,Arial,sans-serif;
    font-size: 2rem;
    line-height: 1.4;
    text-align: center;
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
    error = ''
    if request.method == 'POST':
        str_code = request.form['code']
        code = sanitize(str_code)
        if code is False:
            log('Non-sane "code" received:', str_code)
            error = f'Le code reçu n\'a pas le bon format : {str_code}'
        else:
            url = URL_PER_CODE.get(code)
            if url:
                return redirect(url)
            error = f'Code incorrect : {code:06}'
        error += '\n<br><hr>'
    return BASE_HTML.format(body=f'''{error}
    <form method="POST">
        <label for="code">Entrez le code :</label>
        <br><br>
        <input type="number" name="code" maxlength="6" size="6" pattern="\d{6}" placeholder="123456" required/>
        <br><br>
        <input type="submit"/>
    </form>''')

def sanitize(code: str):
    try:
        code = int(code)
    except:
        return False
    if 0 <= int(code) < 1000000:
        return code
    return False

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
