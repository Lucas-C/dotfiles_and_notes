'''
Generates Markdown tables of 2 interesting measurements of Pandemic cities graph:
- the number of other cities a node is connected to
- the distance to the farthest city per node

The data used to generate the JSON initially comes from:
- https://indicatrix.org/overanalyzing-board-games-network-analysis-and-pandemic-482b2018469
- http://files.indicatrix.org/pandemic.graphml
'''
from collections import defaultdict
import json
from os.path import dirname, join, realpath

from tabulate import tabulate


def stats_tables(json_graph_filepath):
    with open(json_graph_filepath) as json_file:
        graph = json.load(json_file)
    connectivity = [(city, len(edges)) for city, edges in graph.items()]
    connectivity = sorted(connectivity, key=lambda e: '{}{}'.format(10-e[1], e[0]))  # sort numerically by 2nd column (in 0-10) then alphabetically by 1st
    print(tabulate(connectivity,
                   headers=('city', 'connectivity'),
                   tablefmt='pipe'))  # for Markdown tables
    print()
    remoteness = [(city, get_remoteness(city, graph)) for city in graph.keys()]
    remoteness = sorted(remoteness, key=lambda e: '{}{}'.format(10-e[1], e[0]))  # sort numerically by 2nd column (in 0-10) then alphabetically by 1st
    print(tabulate(remoteness,
                   headers=('city', 'remoteness'),
                   tablefmt='pipe'))  # for Markdown tables

def get_remoteness(src_city, graph):
    distance = 0
    visited = set((src_city,))
    while len(visited) != len(graph):
        for start_city in set(visited):
            for neighbour in graph[start_city]:
                visited.add(neighbour)
        distance += 1
    return distance

def graphml2json(graphml_filepath, json_filepath):
    # pygraphml bugs were discovered while writing this: https://github.com/hadim/pygraphml/pull/20
    from pygraphml import GraphMLParser
    parser = GraphMLParser()
    graph = parser.parse(graphml_filepath)
    labels_graph = defaultdict(list)
    for edge in graph.edges():
        labels_graph[edge.node1['label']].append(edge.node2['label'])
        labels_graph[edge.node2['label']].append(edge.node1['label'])
    with open(json_filepath, 'w') as json_file:
        json.dump(labels_graph, json_file)


if __name__ == '__main__':
    pandemic_graph_filepath = join(dirname(realpath(__file__)), 'pandemic_graph.json')
    #graphml2json('pandemic.graphml', pandemic_graph_filepath)
    stats_tables(pandemic_graph_filepath)
