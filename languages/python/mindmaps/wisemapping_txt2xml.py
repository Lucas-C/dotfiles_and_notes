#!/usr/bin/python3

# RUN UNIT TESTS: ./txt2xml.py --self-test DUMMY

import argparse, re, sys
from collections import namedtuple
from itertools import count
from xml.sax.saxutils import quoteattr

from pseudo_markdown_parser import LineGrammar # require pyparsing
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

Topic = namedtuple('Topic', ('text', 'link', 'icons', 'attrs'))

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
    parser.add_argument('--default-img-size', default='80,43')
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
                            default_img_size=args.default_img_size,
                            font_color=args.font_color)
    print('{}<topic {} position="0,0" text={} id="{}">'.format(indent, topic.attrs, quoteattr(topic.text), next(counter)))
    if topic.link:
        print('{}    <link url="{}" urlType="url"/>'.format(indent, topic.link))
    for icon in topic.icons:
        print('{}    <icon id="{}"/>'.format(indent, icon))
    for order, child in enumerate(node.children):
        recursively_print(child, args, height=height, counter=counter, indent=indent, branch_id=branch_id, order=order)
    print('{}</topic>'.format(indent))

def topic_from_line(text_line, edge_width=1, branch_id=None, default_attrs=None, default_img_size='', font_color=''):
    parsed_line = LineGrammar.parseString(text_line, parseAll=True)
    link = parsed_line.url
    attrs = {}
    if default_attrs:
        attrs.update(default_attrs)
    if parsed_line.is_img:
        attrs['shape'] = 'image'
        img_size = '{}x{}'.format(int(parsed_line.img_width), int(parsed_line.img_height)) if parsed_line.img_width and parsed_line.img_height else default_img_size
        attrs['image'] = '{}:{}'.format(img_size, link)
        link = None
    comment_attrs = ''
    if parsed_line.attrs:
        comment_attrs = ' '.join(attr.strip() for attrs in parsed_line.attrs for attr in attrs)
    is_bold, is_italic, is_striked = bool(parsed_line.is_bold), bool(parsed_line.is_italic), bool(parsed_line.is_striked)
    if not comment_attrs and (is_bold or is_italic):
        bold = 'bold' if is_bold else ''
        italic = 'italic' if is_italic else ''
    else:
        bold, italic = '', ''
    if font_color or bold or italic:
        # cf. https://bitbucket.org/wisemapping/wisemapping-open-source/src/master/mindplot/src/main/javascript/persistence/XMLSerializer_Pela.js?at=develop&fileviewer=file-view-default#XMLSerializer_Pela.js-281
        attrs['fontStyle'] = ';;{};{};{};'.format(font_color, bold, italic)
    if branch_id is not None:
        attrs['edgeStrokeColor'] = EDGE_COLORS[branch_id % len(EDGE_COLORS)]
        attrs['edgeStrokeWidth'] = edge_width
    attrs = ' '.join('{}="{}"'.format(k, v) for k, v in sorted(attrs.items()))
    if comment_attrs:
        attrs = attrs + ' ' + comment_attrs if attrs else comment_attrs
    icons = tuple(parsed_line.icons)
    if parsed_line.has_checkbox:
        icons = icons + ('tick_tick' if parsed_line.is_checked else 'tick_cross',)
    return Topic(text=parsed_line.text[0].strip(), link=link or None, icons=icons, attrs=attrs)

def self_test():
    assert topic_from_line('toto') \
            == Topic(text='toto', link=None, icons=(), attrs='')
    assert topic_from_line('[Framindmap](https://framindmap.org)') \
            == Topic(text='Framindmap', link='https://framindmap.org', icons=(), attrs='')
    assert topic_from_line('![coucou](http://website.com/favicon.ico)') \
            == Topic(text='coucou', link=None, icons=(), attrs='image=":http://website.com/favicon.ico" shape="image"')
    assert topic_from_line('!toto') \
            == Topic(text='!toto', link=None, icons=(), attrs='')
    assert topic_from_line('Productivity   !icon=chart_bar <!-- fontStyle=";;#104f11;;;" bgColor="#d9b518" -->') \
            == Topic(text='Productivity', link=None, icons=('chart_bar',), attrs='fontStyle=";;#104f11;;;" bgColor="#d9b518"')
    assert topic_from_line('**toto**') \
            == Topic(text='toto', link=None, icons=(), attrs='fontStyle=";;;bold;;"')
    assert topic_from_line('__toto__') \
            == Topic(text='toto', link=None, icons=(), attrs='fontStyle=";;;;italic;"')
    assert topic_from_line('__**toto**__') \
            == Topic(text='toto', link=None, icons=(), attrs='fontStyle=";;;bold;italic;"')
    assert topic_from_line('**__toto__**') \
            == Topic(text='toto', link=None, icons=(), attrs='fontStyle=";;;bold;italic;"')
    assert topic_from_line('toto !icon=ahoy') \
            == Topic(text='toto', link=None, icons=('ahoy',), attrs='')
    assert topic_from_line('!icon=A toto !icon=B') \
            == Topic(text='toto', link=None, icons=('A', 'B'), attrs='')
    assert topic_from_line('![toto](http://website.com/favicon.ico 600x0400)') \
            == Topic(text='toto', link=None, icons=(), attrs='image="600x400:http://website.com/favicon.ico" shape="image"')
    assert topic_from_line('[x] toto') \
            == Topic(text='toto', link=None, icons=('tick_tick',), attrs='')
    # TODO: require support for https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/text-decoration in mindplot/src/main/javascript/Topic.js line 356 & web2d/src/main/javascript/Text.js line 48
    assert topic_from_line('~~toto~~') \
            == Topic(text='toto', link=None, icons=(), attrs='')
    print('All tests passed')


if __name__ == '__main__':
    main(sys.argv[1:])

