#!/usr/bin/env python3

# Proxy/downloader, used to archive online HTML games that load ressources at runtime, through JS.

import argparse, os, shutil, sys
from functools import partial
from http.server import HTTPStatus, SimpleHTTPRequestHandler, test
from urllib.parse import unquote

import requests

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, base_url, cookie, **kwargs):
        self.base_url = base_url
        self.cookie = cookie
        self.not_found_caught = False
        super().__init__(*args, **kwargs)

    def send_head(self):
        file = super().send_head()
        if file or not self.not_found_caught:
            return file
        self.not_found_caught = False
        path = unquote(self.path)
        url = self.base_url + path
        print('Retrieving missing file from:', url)
        response = requests.get(url, headers={'Cookie': args.cookie}, stream=True)
        if response.status_code != 200:
            super().send_error(response.status_code)
            self.not_found_caught = False
            return None
        response.raw.decode_content = True
        dest_file_path = path[1:]
        dest_dir = os.path.split(dest_file_path)[0]
        if dest_dir:
            os.makedirs(os.path.split(dest_file_path)[0], exist_ok=True)
        with open(dest_file_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        return super().send_head()

    def send_error(self, code, message=None, explain=None):
        if code != HTTPStatus.NOT_FOUND:
            return super().send_error(code, message, explain)
        self.not_found_caught = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('base_url')
    parser.add_argument('--cookie')
    parser.add_argument('--directory', default='.')
    parser.add_argument('--port', type=int, default='8888')
    args = parser.parse_args()
    if args.base_url.endswith('/'):
        args.base_url = args.base_url[:-1]
    handler_class = partial(CustomHTTPRequestHandler,
                            base_url=args.base_url,
                            cookie=args.cookie,
                            directory=args.directory)
    test(HandlerClass=handler_class, port=args.port)
