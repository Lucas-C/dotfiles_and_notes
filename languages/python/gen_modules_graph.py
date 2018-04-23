#!python

# PURPOSE: generate a Python modules graph in JSON to be viewed by https://github.com/fzaninotto/DependencyWheel

# REQUIRES: pip install modulegraph

# USAGE: gen_modules_graph.py httpie.core > modules-graph.json

from __future__ import print_function
import json, os, sys
from modulegraph.modulegraph import ModuleGraph


def build_modules_graph(path, entrypoint_module):
    root_pkg = entrypoint_module.split('.')[0]
    mf = ModuleGraph(path, debug=1)
    mf.import_hook(entrypoint_module)

    packages = {}  # map: name => unique id
    for m in sorted(mf.flatten(), key=lambda n: n.identifier):
        if not m.identifier.startswith(root_pkg + '.'):  # keeping only internal modules
            continue
        module_name = m.identifier.split('.')[-1]
        if module_name == module_name.upper() or module_name.startswith('__'):  # we ignore CONSTANTS & __version__-like metadata
            continue
        if m.identifier not in packages:
            packages[m.identifier] = len(packages)

    n = len(packages)
    matrix = [[0]*n for _ in range(n)]
    for pkg_name, pkg_id in packages.items():
        parent_pkg = '.'.join(pkg_name.split('.')[:-1])
        for outgoing_edge_id in mf.graph.nodes[pkg_name][1]:
            edge_dest_pkg_name = mf.graph.edges[outgoing_edge_id][1]
            if edge_dest_pkg_name != parent_pkg and edge_dest_pkg_name in packages:
                print('Module {} depends on module {}'.format(pkg_name, edge_dest_pkg_name), file=sys.stderr)
                matrix[pkg_id][packages[edge_dest_pkg_name]] += 1

    # we remove all packages that have zero deps to & from other ones
    lone_modules_may_exist = True
    while lone_modules_may_exist:
        lone_modules_may_exist = False
        i = 0
        while i < len(matrix):
            n = len(matrix)  # this value will change as matrix shrinks
            if all(matrix[i][j] == 0 for j in range(n)) and all(matrix[j][i] == 0 for j in range(n)):
                print(i)
                lone_modules_may_exist = True
                packages = {pkg: index for pkg, index in packages.items() if index != i}
                matrix = matrix[:i] + matrix[i+1:]
                for j, row in enumerate(matrix):
                    matrix[j] = row[:i] + row[i+1:]
            i += 1

    modules_graph = {
        'matrix': matrix,
        'packageNames': [p[len(root_pkg)+1:] for p in sorted(packages.keys(), key=lambda name: packages[name])],
    }
    return modules_graph


if __name__ == '__main__':
    print(json.dumps(build_modules_graph(['.'] + sys.path, sys.argv[1])))
