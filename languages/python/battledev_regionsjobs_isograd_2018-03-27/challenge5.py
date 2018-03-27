# A greedy, non-O(n^3) solution
from itertools import combinations
N = int(input())
t = [list(map(int, input().split())) for i in range(N)]
def split(vertices, edge):
    if edge[0] > edge[1]:
        edge = edge[1], edge[0]
    edge_range = range(edge[0]+1, edge[1])
    v_in = {v for v in vertices if v in edge_range and v != edge[0] and v != edge[1]}
    v_out = {v for v in vertices if v not in edge_range and v != edge[0] and v != edge[1]}
    return v_in, v_out
def best_path_length(vertices):
    if len(vertices) <= 1:
        return 0
    best_length = None
    for line in combinations(vertices, 2):
        subgraph1, subgraph2 = split(vertices, line)
        path_length = t[line[0]][line[1]] + best_path_length(subgraph1) + best_path_length(subgraph2)
        if not best_length or path_length > best_length:
            best_length = path_length
    return best_length
print(best_path_length(set(range(N))))
