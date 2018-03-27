from itertools import permutations
pancakes = list(map(int, (input() for _ in range(6))))
if sorted(pancakes) == pancakes:
    print(0)
def enum_moves(max):
    for e in range(1, 7):
        yield [e]
    if max > 1:
        for moves in enum_moves(max-1):
            for e in range(1, 7):
                yield [e] + moves
for moves in enum_moves(max=8):
    moves_count = 0
    p = list(pancakes)
    while moves:
        moves_count += 1
        k = moves.pop()
        p = list(reversed(p[:k])) + p[k:]
    if sorted(p) == p:
        print(moves_count)
        break