#!/usr/bin/python3

# INSTALL: apt install graphviz / apt-cyg install graphviz (Cygwin)
#          pip install pydot
# -> note: this dependancy could easily be removed as generating a .dot graph from a GraphNode
#          and calling twopi should be straightfoward, and allow to display stderr warnings like 'Pango-WARNING **: failed to choose a font, expect ugly output'
# CYGWIN: I had an issue where symptoms were: no characaters rendered, only squares; a Pango-WARNING in twopi stderr; fc-list output empty
# -> solution was to configure fontconfig to use the Windows fonts:
#         apt-cyg install xorg-x11-fonts-Type1 fontconfig
#         cat <<EOF >/etc/fonts/local.conf
#         <?xml version="1.0"?>
#         <!DOCTYPE fontconfig SYSTEM "fonts.dtd">
#         <fontconfig>
#             <dir>/c/Windows/Fonts</dir>
#         </fontconfig>
#         EOF
#         fc-cache --verbose
#         fc-list
# POTENTIAL EXTRA FEATURES: support for basic bold/italic Markdown markup: http://stackoverflow.com/a/30200953/636849

import argparse, pydot, shutil, subprocess, sys


ROOT_DEFAULT_NAME = '<[root]>'


def main(argv):
    print('Using command:', subprocess.check_output([shutil.which('twopi'), '-V'], stderr=subprocess.STDOUT).decode('utf8'), end='', file=sys.stderr)
    args = parse_args(argv)
    if args.self_test:
        self_test(args.input_filepath)
    else:
        kwargs = args.__dict__
        kwargs.pop('self_test')
        create_solarized_mindmap_from_file(**kwargs)


def parse_args(argv):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, fromfile_prefix_chars='@')
    parser.add_argument('--layout', default='twopi', choices=('dot', 'fdp', 'neato', 'sfdp', 'twopi'), help=' ')
    parser.add_argument('--font', default='arial')
    parser.add_argument('--gen-dot-file', action='store_true')
    parser.add_argument('--root-label')
    parser.add_argument('--self-test', action='store_true', help='Test graph parsing on a file or with builtin unit tests')
    parser.add_argument('input_filepath')
    return parser.parse_args(argv)


def create_solarized_mindmap_from_file(input_filepath, layout='twopi', font='arial', gen_dot_file=True, root_label=None):
    with open(input_filepath) as txt_file:
        text = txt_file.read()
    outfile_basename = input_filepath.rsplit('.', 1)[0]
    theme = DarkSolarizedTheme(layout=layout, font=font)
    graph = parse_graph(text, root_label=root_label)
    create_mindmap(graph, outfile_basename, theme=theme, gen_dot_file=gen_dot_file)


def parse_graph(text, root_label=None):
    if not text:
        raise ValueError('Empty graph')
    if text[-1] == '\n':
        text = text[:-1]
    root = GraphNode(root_label or ROOT_DEFAULT_NAME)
    last_nodes_per_depth = {0: root}
    last_node = None
    for i, line in enumerate(text.splitlines()):
        line = line.rstrip()
        value = line.lstrip()
        if not value:
            raise ValueError('Line {} is empty'.format(i + 1))
        indent = len(line) - len(value)
        if indent % 4 != 0:
            raise ValueError('Incorrect indentation on line {}: not a mutiple of 4 spaces'.format(i + 1))
        depth = 1 + indent / 4
        if last_node:
            if last_node.depth + 1 < depth:
                raise ValueError('Incorrect indentation on line {}: too much indent compared to previous line'.format(i + 1))
        else:
            if depth != 1:
                raise ValueError('Incorrect indentation on line {}: first line must not have any indent'.format(i + 1))
        parent_node = last_nodes_per_depth[depth - 1]
        last_node = parent_node.add_child(value)
        last_nodes_per_depth[last_node.depth] = last_node
    return root


class GraphNode:
    last_branch_id = -1
    known_contents = set()

    @classmethod
    def reset(cls):  # for tests
        cls.last_branch_id = -1
        cls.known_contents = set()

    def __init__(self, content=None, parent=None):
        while content and content in self.known_contents:
            print('Duplicate content found: {}. Using workaround'.format(content), file=sys.stderr)
            content = content + ' '
        if ':' in content:
            content = '"{}"'.format(content) # avoid pydot 'port' dectection
        self.known_contents.add(content)
        self.content = content
        self.parent = parent
        self._branch_id = None
        self.children = []

    def add_child(self, content):
        child = self.__class__(content, self)
        self.children.append(child)
        return child

    def set_branch_ids(self):
        self.last_branch_id += 1
        self._branch_id = self.last_branch_id
        for child in self.children:
            self.last_branch_id += 1
            child._branch_id = self.last_branch_id

    @property
    def branch_id(self):
        node = self
        while node._branch_id is None and node.parent:
            node = node.parent
        return node._branch_id

    @property
    def depth(self):
        depth = 0
        node = self
        while node.parent:
            node = node.parent
            depth += 1
        return depth

    @property
    def height(self):
        if not self.children:
            return 1
        return 1 + max(child.height for child in self.children)

    @property
    def is_pre_leaf(self):
        if not self.children:
            return False
        return all(not child.children for child in self.children)

    def __str__(self, indent=''):
        out = indent + self.content + '\n' if self.parent else ''
        if self.parent:
            indent += '    '
        for child in self.children:
            out += child.__str__(indent)
        return out

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child


def create_mindmap(graph, outfile_basename, theme, gen_dot_file):
    if graph.content == ROOT_DEFAULT_NAME and len(graph.children) == 1:
        graph = graph.children[0]
        graph.parent = None
    graph.set_branch_ids()
    graph_height = graph.height
    g = pydot.Dot(root=graph.content, **theme.graph_style)
    for node in graph:
        g.add_node(pydot.Node(node.content, **theme.node_style(node.content, node.depth, node.branch_id, graph_height)))
        if node.parent:
            g.add_edge(pydot.Edge(node.parent.content, node.content, **theme.edge_style(node.depth, node.branch_id, graph_height)))
    if gen_dot_file:
        dot_outfile = '{}.dot'.format(outfile_basename)
        print('Generating', dot_outfile, file=sys.stderr)
        g.write(dot_outfile, prog='twopi')
    png_outfile = '{}.png'.format(outfile_basename)
    print('Generating', png_outfile, file=sys.stderr)
    g.write_png(png_outfile, prog='twopi')


class DarkSolarizedTheme:
    DARKGREYBLUE = '#012b37'
    GREY = '#939393'
    # Palette from http://ethanschoonover.com/solarized
    YELLOW = '#b58900'
    ORANGE = '#cb4b16'
    RED = '#dc323f'
    MAGENTA = '#d33682'
    VIOLET = '#6c71c4'
    BLUE = '#268bd2'
    CYAN = '#2aa198'
    GREEN = '#859900'

    EDGE_COLORS = [YELLOW, ORANGE, VIOLET, RED, BLUE, MAGENTA, CYAN, GREEN, GREY]

    def __init__(self, layout, font):
        self.graph_style = dict(
            layout = layout,
            overlap = 'false',
            splines = 'curved',
            fontname = font,
            bgcolor = self.DARKGREYBLUE,
        )

    def edge_style(self, src_depth, branch_id, graph_height):
        return dict(
            color=self.EDGE_COLORS[branch_id % len(self.EDGE_COLORS)],
            dir='none',
            penwidth=2 * (2 + graph_height - src_depth),
        )

    def node_style(self, content, depth, branch_id, graph_height):
        label = content.strip() if content and content != ROOT_DEFAULT_NAME else ''
        return dict(
            group=branch_id,
            shape='plaintext',
            label=label,
            fontcolor='white',
            fontsize=2 * (16 + graph_height - depth),
            fontname=self.graph_style['fontname'], # not inherited by default
        )


def self_test(input_filepath):
    with open(input_filepath) as txt_file:
        text = txt_file.read()
    if text[-1] == '\n':
        text = text[:-1]
    graph = parse_graph(text)
    out = [l.rstrip() for l in str(graph).splitlines()]
    expected = [l.rstrip() for l in text.splitlines()]
    from difflib import context_diff
    print('\n'.join(context_diff(expected, out)))
    assert out == expected

    text = 'A\n    1\n    2\nB\n    3\n        é'
    graph_root = parse_graph(text)
    print(graph_root)
    assert len(graph_root.children) == 2
    assert len(graph_root.children[0].children) == 2
    assert graph_root.children[0].children[0].depth == 2
    GraphNode.reset()
    parse_graph(text + '\n')
    GraphNode.reset()
    parse_graph('A\n    1\nB    A')
    GraphNode.reset()
    try:
        parse_graph('')
        assert False
    except ValueError:
        pass
    GraphNode.reset()
    try:
        parse_graph('\n\n')
        assert False
    except ValueError:
        pass
    GraphNode.reset()
    try:
        parse_graph('    A')
        assert False
    except ValueError:
        pass
    GraphNode.reset()
    try:
        parse_graph('A\n  B')
        assert False
    except ValueError:
        pass
    GraphNode.reset()
    try:
        parse_graph('A\n        B')
        assert False
    except ValueError:
        pass


if __name__ == "__main__":
    main(sys.argv[1:])
