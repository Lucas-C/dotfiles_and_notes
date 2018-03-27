# Suboptimal solution found at 21:59 on 2018/03/27
N = int(input())
t = [list(map(int, input().split())) for i in range(N)]
edges_scores = [(i, sum(t[i][j] for j in range(N))) for i in range(N)]
best_edges = [e[0] for e in sorted(edges_scores, key=lambda e: e[1], reverse=True)]
print(best_edges)
def lines_crossing(l1, l2):
    l2_range = range(*l2) if l2[0] < l2[1] else range(l2[1], l2[0])
    l1_a_inside = l1[0] in l2_range
    l1_b_inside = l1[1] in l2_range
    return (l1_a_inside and l1_b_inside) or (not l1_a_inside and not l1_b_inside)
def lines_passengers_total(path):
    return sum(t[l[0]][l[1]] for l in path)
def recur_build_path(path, best_edges):
    if len(best_edges) <= 1:
        return path
    for i, edge1 in enumerate(best_edges):
        for edge2 in best_edges[i+1:]:
            line = (edge1, edge2)
            if any(lines_crossing(line, l) for l in path):
                continue
            edges = list(best_edges)
            edges.remove(edge1)
            edges.remove(edge2)
            full_path = recur_build_path(path|{line}, edges)
            if full_path:
                return full_path
    return None
path = recur_build_path(set(), best_edges)
print(path)
print(lines_passengers_total(path))
# max_passengers = 0
# for passengers_count in enum_lines_for_graph(set(range(N)), set()):
    # if passengers_count > max_passengers:
        # max_passengers = passengers_count
# print(max_passengers)