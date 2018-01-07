import http.server, socketserver

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        nbytes = int(self.headers.get('content-length', '0'))
        data = self.rfile.read(nbytes) if nbytes else None
        print('POST data:', data)
        self.send_response(http.HTTPStatus.FOUND)  # 302
        self.send_header('Location', self.path)
        self.end_headers()

with socketserver.TCPServer(('', 8000), Handler) as httpd:
    httpd.serve_forever()
