#!/usr/bin/env python3
import http, json, os, re, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, unquote

class JsonHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path, resp_body = self._extract_base_resp_body()
        if path.startswith('/status'):
            _, status = path.rsplit('/', 1)
            self._send_response(b'', status=int(status))
        elif path == '/get':
            self._send_ok_json_response(resp_body)
    def do_POST(self):
        path, resp_body = self._extract_base_resp_body()
        resp_body['data'] = ''
        resp_body['files'] = {}
        resp_body['form'] = {}
        resp_body['json'] = None
        nbytes = int(self.headers.get('content-length', '0'))
        data = self.rfile.read(nbytes) if nbytes else b''
        content_type = self.headers.get('content-type')
        if content_type == 'application/json':
            resp_body['data'] = data.decode('utf8')
            try:
                resp_body['json'] = json.loads(data)
            except:
                pass
        elif content_type == 'application/x-www-form-urlencoded':
            resp_body['form'] = {k.decode('utf8'): v.decode('utf8') for k,v in parse_qsl(data, True)}
        self._send_ok_json_response(resp_body)
    def _extract_base_resp_body(self):
        path, _, query_string = self.path.partition('?')
        return path, {
            'args': dict(parse_qsl(query_string, True)),
            'headers': {k: str(v) for k, v in self.headers.items()},
            'origin': self.connection.getpeername()[0],
            'url': 'http://httpbin' + self.path,
        }
    def _send_ok_json_response(self, resp_body):
        self._send_response(json.dumps(resp_body, indent=2, sort_keys=True).encode('utf8') + b'\n', content_type='application/json')
    def _send_response(self, body, status=http.HTTPStatus.OK, content_type='text/html; charset=utf-8'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)
        self.wfile.flush()

if __name__ == '__main__':
    HOST_NAME = os.environ.get('HOST', '0.0.0.0')
    PORT_NUMBER = int(os.environ.get('PORT', '8000'))
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), JsonHandler)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))
