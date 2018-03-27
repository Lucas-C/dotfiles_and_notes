# A greedy, non-O(n^3) solution
from itertools import combinations
N = int(input())
t = [list(map(int, input().split())) for i in range(N)]
MAX = max(max(row) for row in t)
def split(vertices, edge):
    if edge[0] > edge[1]:
        edge = edge[1], edge[0]
    edge_range = range(edge[0]+1, edge[1])
    v_in = frozenset(v for v in vertices if v in edge_range and v != edge[0] and v != edge[1])
    v_out = frozenset(v for v in vertices if v not in edge_range and v != edge[0] and v != edge[1])
    return v_in, v_out
cache = {}
cache_hits = 0
def best_path_length(vertices, length_so_far=0, length_to_beat=None):
    if len(vertices) <= 1:
        return 0
    if len(vertices) == 2:
        l = list(vertices)
        return t[l[0]][l[1]]
    max_expectable_lines_count = len(vertices) // 2
    if length_to_beat:
        if max_expectable_lines_count <= 10:  # if there aren't too many possible values, we calculate a precise achievable max
            max_expectable_length = sum(list(sorted((t[i][j] for i in vertices for j in vertices), reverse=True))[:max_expectable_lines_count])
        else:  # we fallback to a more approximative optimal estimation
            max_expectable_length = max_expectable_lines_count * MAX
        if length_so_far + max_expectable_length < length_to_beat:
            print('Branch cut at depth:', len(vertices))
            return 0  # totally ineffective with input4.txt
    global cache_hits
    if vertices in cache:
        cache_hits += 1
        return cache[vertices]
    best_length = None
    for line in combinations(vertices, 2):
        line_length = t[line[0]][line[1]]
        subgraph1, subgraph2 = split(vertices, line)
        path_length = line_length + best_path_length(subgraph1, length_so_far+line_length, best_length) + best_path_length(subgraph2, length_so_far+line_length, best_length)
        if not best_length or path_length > best_length:
            best_length = path_length
    cache[vertices] = best_length
    return best_length
try:
    print(best_path_length(frozenset(range(N))))
finally:
    print('len(cache):', len(cache))
    print('cache_hits:', cache_hits) # after 1m30, we get a 100Mo cache containing 100 000 entries reused in avg 40 times
