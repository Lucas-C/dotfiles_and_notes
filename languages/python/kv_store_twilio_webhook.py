# Inspired by rpg-bonhomme
#   curl -v -XPOST -F Body=Boo http://chezsoi.org/lucas/brain-dump/webhook
#   curl -v -XPOST -F Body=Boo$'\n'Dummy http://chezsoi.org/lucas/brain-dump/webhook
#   curl -v -XPOST -F Body=Boo http://chezsoi.org/lucas/brain-dump/webhook

import cgi, logging, logging.handlers, os, re, sqlite3, traceback
from configobj import ConfigObj
from collections import namedtuple
from contextlib import closing
from threading import Lock
try:
    from urlparse import parse_qsl
except ImportError:
    from urllib.parse import parse_qsl

SCRIPT_DIR = os.path.dirname(__file__) or '.'
CONFIG = ConfigObj(os.path.join(SCRIPT_DIR, re.sub('.pyc?$', '.ini', __file__)))
DATABASE_FILE = os.path.join(SCRIPT_DIR, CONFIG.get('db_file'))
LOG_FILE = os.path.join(SCRIPT_DIR, CONFIG.get('log_file'))
LOG_FORMAT = '%(asctime)s - %(process)s [%(levelname)s] %(filename)s %(lineno)d %(message)s'
MAX_KEY_LENGTH = CONFIG.as_int('max_key_length')
MAX_VALUE_LENGTH = CONFIG.as_int('max_value_length')
MAX_TABLE_SIZE = CONFIG.as_int('max_table_size')

def application(env, start_response):
    path = env.get('PATH_INFO', '')
    method = env['REQUEST_METHOD']
    query_params = parse_query_string(env['QUERY_STRING'])
    form = pop_form(env)
    log('Handling request: {} "{}" with query_params: "{}", form: "{}"'.format(method, path, query_params, form))
    http_return_code = '200 OK'
    try:
        response = handle_request(method, path, query_params, form)
    except Exception:
        error_msg = traceback.format_exc()
        log('[ERROR] : {}'.format(error_msg), logging.ERROR)
        http_return_code = '500 Internal Server Error'
        response = cgi.escape(error_msg)
    start_response(http_return_code, [('Content-Type', 'application/xml')])
    return [wrap_in_twiml(response).encode('utf8')]

def wrap_in_twiml(msg):
    response = '<Message>' + msg + '</Message>' if msg else ''
    return '<?xml version="1.0" encoding="UTF-8"?><Response>' + response + '</Response>'

def pop_form(env):
    """
    Should be called only ONCE because reading env['wsgi.input'] will empty the stream,
    hence we pop the value
    """
    if 'wsgi.input' not in env:
        return None
    post_env = env.copy()
    post_env['QUERY_STRING'] = ''
    form = cgi.FieldStorage(
        fp=env.pop('wsgi.input'),
        environ=post_env,
        keep_blank_values=True
    )
    return {k: form[k].value for k in form}

def parse_query_string(query_string):
    qprm = dict(parse_qsl(query_string, True))
    return {k: qprm[k] for k in qprm}

def handle_request(method, path, query_params, form):
    assert method == 'POST'
    assert path == '/'
    assert not query_params
    assert 'Body' in form
    text = form['Body']
    key, new_value = text.split('\n', 1) if '\n' in text else (text, '')
    log('GET key="{}"'.format(key))
    current_value = db_get(key)
    log('-> ' + str(current_value))
    if not new_value:  # => simple RETRIEVE request
        return key + '\n' + current_value
    # At this point, it's either a CREATE request or a valid UPDATE request
    log('PUT key="{}":value="{}"'.format(key, new_value))
    db_put(key, new_value)

def db_get(key):
    with closing(_DB.cursor()) as db_cursor:
        db_cursor.execute('SELECT Value FROM KVStore WHERE Key=?', (key,))
        query_result = db_cursor.fetchone()
    if not query_result or len(query_result) != 1:
        return None
    return str(query_result[0])

def db_put(key, value):
    db_check_table_size()
    with closing(_DB.cursor()) as db_cursor:
        db_cursor.execute('INSERT OR REPLACE INTO KVStore VALUES (?, ?)', (key, value))
        _DB.commit()

def db_list_keys():
    with closing(_DB.cursor()) as db_cursor:
        db_cursor.execute('SELECT Key FROM KVStore')
        return db_cursor.fetchall()

def db_check_table_size():
    with closing(_DB.cursor()) as db_cursor:
        db_cursor.execute('SELECT COUNT(*) FROM KVStore')
        query_result = db_cursor.fetchone()
    table_size = int(query_result[0])
    if MAX_TABLE_SIZE and table_size > MAX_TABLE_SIZE:
        raise MemoryError('Table size exceeded limit: {} > {}'.format(table_size, MAX_TABLE_SIZE))

def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 ** 2, backupCount=10)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)
    return logger

def log(msg, lvl=logging.INFO):
    with _LOGGER_LOCK:
        _LOGGER.log(lvl, msg)

_LOGGER = configure_logger()
_LOGGER_LOCK = Lock()
_DB = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
log('Starting : {} keys found in the DB - Config: {}'.format(len(db_list_keys()), CONFIG))
