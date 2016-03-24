import sys
def local_print(*args):
    print(*args, file=sys.stderr)
local_print('** TOPSTART **')
n = int(input())
P = list(map(int, input().split(' ')))
local_print(','.join(map(str, P)))
assert len(P) == n
T = sum(P)
pipo_components = []
for component_size in P:
    components = set()
    pipo_components.append(components)
    for pipo in range(component_size):
        pipo = input()
        local_print(pipo)
        components.add(pipo)
Q = int(input())
pipos_sentences_count = 0

def recur_is_pipo(sentence, pipo_components_left):
    if not pipo_components_left:
        return not sentence
    while pipo_components_left:
        components = pipo_components_left.pop(0)
        for pipo in components:
            if not sentence.startswith(pipo):
                continue
            local_print('a pipo:', pipo, len(pipo_components_left))
            if recur_is_pipo(sentence[len(pipo) + 1:], pipo_components_left.copy()):
                return True

for _ in range(Q):
    sentence = input()
    local_print('START')
    local_print(sentence)
    curr_pipo_components = pipo_components.copy()
    if recur_is_pipo(sentence, pipo_components.copy()):
        local_print('RESULT: OK')
        pipos_sentences_count += 1
    else:
        local_print('RESULT: KO')
print(pipos_sentences_count)