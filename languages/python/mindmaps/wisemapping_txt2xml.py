#!/usr/bin/python3

# RUN UNIT TESTS: ./txt2xml.py --self-test DUMMY

import argparse, re, sys
from collections import namedtuple
from itertools import count
from txt_mindmap import parse_graph


LINE_PATTERN = (
'('
  '('
    '(?P<is_img>!?)' # optional Markdown image marker
    '\[(?P<link_text>[^][]*)\]' # Markdown link text
    '\((?P<link_url>[^)]+)\)'  # Markdown link URL
  ')|(' # or
    '(?P<is_italic>__)?'
    '(?P<is_bold>\*\*)?'
    '(?P<bare_text>.*?)' # bare text, non-greedy wildcard
    '(\*\*)?'
    '(__)?'
  ')'
')'
'\s*' # extra optional whitespaces
'(\s!icon=(?P<icon>[^\s]+))?' # !icon=...
'\s*' # extra optional whitespaces
'(\s<!--(?P<attrs>.+)-->)?' # extra XML attributes inbetwen comments
'\s*' # extra optional whitespaces
'$'  # parse whole line until last char
)

Topic = namedtuple('Topic', ('text', 'link', 'icon', 'attrs'))


def main(argv):
    args = parse_args(argv)
    if args.self_test:
        return self_test()
    with open(args.input_filepath, encoding='utf8') as txt_file:
        graph = parse_graph(txt_file.read())
    print('<map name="{}" version="tango">'.format(args.name))
    recursively_print(graph, args, indent='', counter=count())
    print('</map>')

def parse_args(argv):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, fromfile_prefix_chars='@')
    parser.add_argument('--name', default='mindmap')
    parser.add_argument('--images-size', default='80,43')
    parser.add_argument('--no-shrink', action='store_false', dest='shrink')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('input_filepath')
    return parser.parse_args(argv)

def recursively_print(node, args, indent, counter, order=None):
    indent += '    '
    attrs = {}
    if order is None:
        attrs['central'] = 'true'
    else:
        attrs['order'] = order
        if args.shrink:
            attrs['shrink'] = 'true'
    topic = topic_from_line(node.content, default_attrs=attrs, images_size=args.images_size)
    print('{}<topic {} position="0,0" text="{}" id="{}">'.format(indent, topic.attrs, topic.text, next(counter)))
    if topic.link:
        print('{}    <link url="{}" urlType="url"/>'.format(indent, topic.link))
    if topic.icon:
        print('{}    <icon id="{}"/>'.format(indent, topic.icon))
    for order, child in enumerate(node.children):
        recursively_print(child, args, indent, counter, order)
    print('{}</topic>'.format(indent))

def topic_from_line(text_line, default_attrs=None, images_size=''):
    re_match = re.match(LINE_PATTERN, text_line)
    text = re_match.group('link_text') or re_match.group('bare_text')
    link, icon = re_match.group('link_url'), re_match.group('icon')
    attrs = {}
    if default_attrs:
        attrs.update(default_attrs)
    if re_match.group('is_img'):
        attrs['shape'] = 'image'
        attrs['image'] = '{}:{}'.format(images_size, link)
        link = None
    comment_attrs = re_match.group('attrs')
    if not comment_attrs and (re_match.group('is_bold') or re_match.group('is_italic')):
        bold = 'bold' if re_match.group('is_bold') else ''
        italic = 'italic' if re_match.group('is_italic') else ''
        attrs['fontStyle'] = ';;;{};{};'.format(bold, italic)
    attrs = ' '.join('{}="{}"'.format(k, v) for k, v in sorted(attrs.items()))
    if comment_attrs:
        attrs = attrs + ' ' + comment_attrs if attrs else comment_attrs
    return Topic(text=text, link=link, icon=icon, attrs=attrs)

def self_test():
    assert topic_from_line('toto') \
            == Topic(text='toto', link=None, icon=None, attrs='')
    assert topic_from_line('[Framindmap](https://framindmap.org)') \
            == Topic(text='Framindmap', link='https://framindmap.org', icon=None, attrs='')
    assert topic_from_line('![coucou](http://website.com/favicon.ico)') \
            == Topic(text='coucou', link=None, icon=None, attrs='image=":http://website.com/favicon.ico" shape="image"')
    assert topic_from_line('!toto') \
            == Topic(text='!toto', link=None, icon=None, attrs='')
    assert topic_from_line('Productivity   !icon=chart_bar <!--fontStyle=";;#104f11;;;" bgColor="#d9b518"-->') \
            == Topic(text='Productivity', link=None, icon='chart_bar', attrs='fontStyle=";;#104f11;;;" bgColor="#d9b518"')
    assert topic_from_line('**toto**') \
            == Topic(text='toto', link=None, icon=None, attrs='fontStyle=";;;bold;;"')
    assert topic_from_line('__toto__') \
            == Topic(text='toto', link=None, icon=None, attrs='fontStyle=";;;;italic;"')
    assert topic_from_line('__**toto**__') \
            == Topic(text='toto', link=None, icon=None, attrs='fontStyle=";;;bold;italic;"')
    assert topic_from_line('**__toto__**') \
            == Topic(text='__toto__', link=None, icon=None, attrs='fontStyle=";;;bold;;"')
    print('All tests passed')


if __name__ == '__main__':
    main(sys.argv[1:])

