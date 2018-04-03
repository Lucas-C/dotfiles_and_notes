# Code fixed after seeing the isograd solution that uses functools.lru_cache:
# I had a good intuition but didn't need combinatorials nor sets !
# Simplicity is key...
import sys
def local_print(*args): print(*args, file=sys.stderr)
N = int(input())
t = [list(map(int, input().split())) for i in range(N)]
cache = {}
cache_hits = 0
def best_path_length(start, end):
    if start + 1 >= end:
        return 0
    if (start, end) in cache:
        global cache_hits
        cache_hits += 1
        return cache[(start, end)]
    best_length = None
    for k in range(start + 1, end):
        line_length = t[start][k]
        path_length = line_length + best_path_length(start + 1, k) + best_path_length(k + 1, end)
        if not best_length or path_length > best_length:
            best_length = path_length
    cache[(start, end)] = best_length
    return best_length
try:
    print(best_path_length(0, N))
finally:
    local_print('len(cache):', len(cache))
    local_print('cache_hits:', cache_hits) # after 1m30, we get a 100Mo cache containing 100 000 entries reused in avg 40 times
