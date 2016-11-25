# Solver recipe from: http://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php
import sys
from functools import total_ordering

def local_print(msg): print(msg, file=sys.stderr)

@total_ordering
class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.distance == other.distance
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.distance < other.distance
        return NotImplemented

    def __hash__(self):
            return self.id

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return

def shortest_proba(v, p=1.0):
    ''' make shortest path from v.previous'''
    if v.previous:
        p = (1.0 - v.get_weight(v.previous))*p
        p = shortest_proba(v.previous, p=p)
    return p

import heapq

def dijkstra(aGraph, start, target):
    '''Dijkstra's shortest path'''
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        #for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                # 'updated : current = %s next = %s new_dist = %s' %(current.get_id(), next.get_id(), next.get_distance())
            else:
                pass# 'not updated : current = %s next = %s new_dist = %s' %(current.get_id(), next.get_id(), next.get_distance())

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)

N = int(input())
A, B = list(map(float, input().split(' ')))

g = Graph()
for i in range(N):
    g.add_vertex(i)
for i in range(N):
    for j, p in enumerate(map(float, input().split(' '))):
        g.add_edge(i, j, p)

local_print('Graph data:')
for v in g:
    for w in v.get_connections():
        vid = v.get_id()
        wid = w.get_id()
        local_print('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))

dijkstra(g, g.get_vertex(A), g.get_vertex(B))
target = g.get_vertex(B)

path = [target.get_id()]
shortest(target, path)
local_print('The shortest path : %s' %(path[::-1]))

final_p = 1 - shortest_proba(target)
print(round(final_p, 3))
