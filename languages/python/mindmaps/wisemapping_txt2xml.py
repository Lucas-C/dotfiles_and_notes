#!/usr/bin/python3

# RUN UNIT TESTS: ./txt2xml.py --self-test DUMMY
# OPTIONAL FEATURES TO IMPLEMENT: support for multiple icons

import argparse, re, sys
from collections import namedtuple
from itertools import count
from xml.sax.saxutils import quoteattr

from txt_mindmap import parse_graph

EDGE_COLORS = ( # dark solarized palette from http://ethanschoonover.com/solarized
    '#b58900', # yellow
    '#cb4b16', # orange
    '#6c71c4', # violet
    '#dc323f', # red
    '#268bd2', # blue
    '#d33682', # magenta
    '#2aa198', # cyan
    '#859900', # green
    '#939393', # grey
)

# Limitations of REGEXs
# - positional : immutable order of !icon & <! --attrs-->
# - now way to parse combinations of bold/italic/Markdown link
# - does not handle repetition, e.g. for !icon=
# => use pyparsing instead: http://infohost.nmt.edu/tcc/help/pubs/pyparsing/web/index.html
LINE_PATTERN = (
'('
  '('
    '(?P<is_img>!?)' # optional Markdown image marker
    '\[(?P<link_text>[^][]*)\]' # Markdown link text
    '\((?P<link_url>[^)]+)\)'  # Markdown link URL
  ')|(' # or
    '(?P<is_italic>(__)?)'
    '(?P<is_bold>(\*\*)?)'
    '(?P<bare_text>.*?)' # bare text, non-greedy wildcard
    '(?P=is_bold)'
    '(?P=is_italic)'
  ')'
')'
'\s*' # extra optional whitespaces
'(\s!icon=(?P<icon>[^\s]+))*' # !icon=...
'\s*' # extra optional whitespaces
'(\s<!--(?P<attrs>.+)-->)*' # extra XML attributes inbetwen comments
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
    recursively_print(graph, args, height=graph.height, counter=count())
    print('</map>')

def parse_args(argv):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, fromfile_prefix_chars='@')
    parser.add_argument('--name', default='mindmap')
    parser.add_argument('--images-size', default='80,43')
    parser.add_argument('--no-shrink', action='store_false', dest='shrink')
    parser.add_argument('--font-color', default='')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('input_filepath')
    return parser.parse_args(argv)

def recursively_print(node, args, height, counter, indent='', branch_id=None, order=None):
    indent += '    '
    attrs = {}
    if order is None:
        attrs['central'] = 'true'
    else:
        attrs['order'] = order
        if branch_id is None:
            branch_id = order
        if args.shrink:
            attrs['shrink'] = 'true'
    topic = topic_from_line(node.content,
                            edge_width=2*(height-indent.count('    ')),
                            branch_id=branch_id,
                            default_attrs=attrs,
                            images_size=args.images_size,
                            font_color=args.font_color)
    print('{}<topic {} position="0,0" text={} id="{}">'.format(indent, topic.attrs, quoteattr(topic.text), next(counter)))
    if topic.link:
        print('{}    <link url="{}" urlType="url"/>'.format(indent, topic.link))
    if topic.icon:
        print('{}    <icon id="{}"/>'.format(indent, topic.icon))
    for order, child in enumerate(node.children):
        recursively_print(child, args, height=height, counter=counter, indent=indent, branch_id=branch_id, order=order)
    print('{}</topic>'.format(indent))

def topic_from_line(text_line, edge_width=1, branch_id=None, default_attrs=None, images_size='', font_color=''):
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
    if comment_attrs:
        comment_attrs = comment_attrs.strip()
    if not comment_attrs and (re_match.group('is_bold') or re_match.group('is_italic')):
        bold = 'bold' if re_match.group('is_bold') else ''
        italic = 'italic' if re_match.group('is_italic') else ''
    else:
        bold, italic = '', ''
    if font_color or bold or italic:
        attrs['fontStyle'] = ';;{};{};{};'.format(font_color, bold, italic)
    if branch_id is not None:
        attrs['edgeStrokeColor'] = EDGE_COLORS[branch_id % len(EDGE_COLORS)]
        attrs['edgeStrokeWidth'] = edge_width
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
    assert topic_from_line('Productivity   !icon=chart_bar <!-- fontStyle=";;#104f11;;;" bgColor="#d9b518" -->') \
            == Topic(text='Productivity', link=None, icon='chart_bar', attrs='fontStyle=";;#104f11;;;" bgColor="#d9b518"')
    assert topic_from_line('**toto**') \
            == Topic(text='toto', link=None, icon=None, attrs='fontStyle=";;;bold;;"')
    assert topic_from_line('__toto__') \
            == Topic(text='toto', link=None, icon=None, attrs='fontStyle=";;;;italic;"')
    assert topic_from_line('__**toto**__') \
            == Topic(text='toto', link=None, icon=None, attrs='fontStyle=";;;bold;italic;"')
    assert topic_from_line('**__toto__**') \
            == Topic(text='__toto__', link=None, icon=None, attrs='fontStyle=";;;bold;;"')
    assert topic_from_line('toto !icon=ahoy') \
            == Topic(text='toto', link=None, icon='ahoy', attrs='')
    assert topic_from_line('!icon=A toto !icon=B') \
            == Topic(text='toto', link=None, icon='B', attrs='')
    print('All tests passed')


if __name__ == '__main__':
    main(sys.argv[1:])

