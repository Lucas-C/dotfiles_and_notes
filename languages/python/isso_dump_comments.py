#!/usr/bin/env python3
import argparse, sqlite3, sys
from collections import defaultdict, namedtuple
from datetime import date
from textwrap import indent
class ColorFallback():
    __getattr__ = lambda self, name: ''
try:
    from colorama import Fore, Style, init
    init()  # for Windows
except ImportError:  # fallback so that the imported classes always exist
    Fore = Style = ColorFallback()


Comment = namedtuple('Comment', ('uri', 'id', 'parent', 'created', 'text', 'author', 'email', 'website', 'likes', 'dislikes', 'replies'))

INDENT = '    '
QUERY = 'SELECT uri, comments.id, parent, created, text, author, email, website, likes, dislikes FROM comments INNER JOIN threads on comments.tid = threads.id'


def main():
    args = parse_args()
    if not args.colors:
        global Fore, Style
        Fore = Style = ColorFallback()
    db = sqlite3.connect(args.db_path)
    comments_per_uri = defaultdict(list)
    for result in db.execute(QUERY).fetchall():
        comment = Comment(*result, replies=[])
        comments_per_uri[comment.uri].append(comment)
    for uri, comments in comments_per_uri.items():
        comments_per_id = {comment.id: comment for comment in comments}
        root_comments = []
        for comment in comments:
            if comment.parent:
                comments_per_id[comment.parent].replies.append(comment)
            else:
                root_comments.append(comment)
        print(Fore.MAGENTA + args.url_prefix + uri + Fore.RESET)
        for comment in root_comments:
            print_comment(INDENT, comment)
            for comment in comment.replies:
                print_comment(INDENT * 2, comment)
        print()

def print_comment(prefix, comment):
    when = date.fromtimestamp(comment.created)
    print(prefix + f'{Style.BRIGHT}{comment.author or "Anonymous"}{Style.RESET_ALL} - {comment.email or ""} {comment.website or ""} {when} +{comment.likes}/-{comment.dislikes}')
    print(indent(comment.text, prefix))

def parse_args():
    parser = argparse.ArgumentParser(description='Dump all Isso comments in chronological order, grouped by replies',
                                     formatter_class=ArgparseHelpFormatter)
    parser.add_argument('db_path', help='File path to Isso Sqlite DB')
    parser.add_argument('--url-prefix', default='', help='Optional domain name to prefix to pages URLs')
    parser.add_argument('--no-colors', action='store_false', dest='colors', default=True, help='Optional domain name to prefix to pages URLs')
    return parser.parse_args()

class ArgparseHelpFormatter(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


if __name__ == '__main__':
    main()
