#!/usr/bin/python3

# RUN UNIT TESTS: ./txt_mindmap.py mindmap.txt


import sys


def parse_graph(text, root_label=None):
    if not text:
        raise ValueError('Empty graph')
    if text[-1] == '\n':
        text = text[:-1]
    root = GraphNode.create_root(root_label)
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
    return root.set_single_child_as_root()


class GraphNode:
    ROOT_DEFAULT_NAME = '<[root]>'

    @classmethod
    def create_root(cls, content):
        return cls(content or cls.ROOT_DEFAULT_NAME, parent=None, branch_id=0, known_contents=set())

    def __init__(self, content, parent, branch_id=None, known_contents=None):
        self.content = content
        self.parent = parent
        self.children = []
        self._branch_id = branch_id
        self._last_branch_id = branch_id
        self._known_contents = known_contents

    def add_child(self, content):
        while content and content in self.known_contents:
            print('Duplicate content found: {}. Using workaround'.format(content), file=sys.stderr)
            content = content + ' '
        self.known_contents.add(content)
        branch_id = None if self.parent else self.incr_last_branch_id()
        child = self.__class__(content, parent=self, branch_id=branch_id)
        self.children.append(child)
        return child

    def set_single_child_as_root(self):
        assert not self.parent, 'This should only be called on a graph root'
        if self.content != self.ROOT_DEFAULT_NAME or len(self.children) != 1:
            return self
        old_root = self
        new_root = old_root.children[0]
        new_root._known_contents = old_root._known_contents
        new_root.parent = None
        new_root._reset_branch_ids()
        return new_root

    def _reset_branch_ids(self):
        assert not self.parent, 'This should only be called on a graph root'
        self._branch_id = 0
        self._last_branch_id = 0
        for child in self.children:
            child._branch_id = self.incr_last_branch_id()

    @property
    def branch_id(self):
        node = self
        while node._branch_id is None and node.parent:
            node = node.parent
        return node._branch_id

    @property
    def known_contents(self):
        node = self
        while node._known_contents is None and node.parent:
            node = node.parent
        return node._known_contents

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

    def incr_last_branch_id(self):
        node = self
        while node._last_branch_id is None and node.parent:
            node = node.parent
        node._last_branch_id += 1
        return node._last_branch_id

    def __str__(self, indent=''):
        should_indent = self.content and self.content != self.ROOT_DEFAULT_NAME
        out = indent + self.content + '\n' if should_indent else ''
        if should_indent:
            indent += '    '
        for child in self.children:
            out += child.__str__(indent)
        return out

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child


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
    parse_graph(text + '\n')
    parse_graph('A\n    1\nB    A')
    try:
        parse_graph('')
        assert False
    except ValueError:
        pass
    try:
        parse_graph('\n\n')
        assert False
    except ValueError:
        pass
    try:
        parse_graph('    A')
        assert False
    except ValueError:
        pass
    try:
        parse_graph('A\n  B')
        assert False
    except ValueError:
        pass
    try:
        parse_graph('A\n        B')
        assert False
    except ValueError:
        pass
    print('All tests passed')


if __name__ == "__main__":
    self_test(sys.argv[1])

