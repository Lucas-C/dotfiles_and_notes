# PURPOSE: generate a Python modules graph in JSON to be viewed by https://github.com/fzaninotto/DependencyWheel

# REQUIRES: pip install modulegraph

# USAGE: python gen_modules_graph.py flaskapp > infralib_packages.json

from __future__ import print_function
import json, os, sys
from modulegraph.modulegraph import ModuleGraph


def build_modules_graph(path, root_pkg):
    mf = ModuleGraph(path, debug=1)
    mf.import_hook(root_pkg)

    packages = {}  # map: name => unique id
    for m in sorted(mf.flatten(), key=lambda n: n.identifier):
        if m.identifier.startswith(root_pkg + '.'):  # filtering only internal modules
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

    # add small increment to equally weighted dependencies to force order
    # (recipe from: https://github.com/fzaninotto/DependencyWheel/blob/master/js/composerBuilder.js#L74 )
    for index, row in enumerate(matrix):
        increment = 0.001
        for i in range(-1, n):
            ii = (i + index) % n
            if row[ii] == 1:
                row[ii] += increment
                increment += 0.001

    modules_graph = {
        'matrix': matrix,
        'packageNames': [p[len(root_pkg)+1:] for p in sorted(packages.keys(), key=lambda name: packages[name])],
    }
    return modules_graph


if __name__ == '__main__':
    print(json.dumps(build_modules_graph(sys.path[1:], sys.argv[1])))
