#!/usr/bin/python3

from collections import defaultdict

def iter_int_pairs(start=1):
    i, j = start, start
    while True:
        yield i, j
        if i == j:
            j += 1
            i = start
        else:
            i += 1

def iter_pythagore_quartets(pairs_count=2):
    square_roots = defaultdict(list)
    for i, j in iter_int_pairs():
        square = i**2 + j **2
        roots = square_roots[square]
        roots.append((i, j))
        if len(roots) == pairs_count:
            yield roots

def main():
    print('Smallest integers N so that there exist a,b,c,d such as N = a² + b² = c² + d² :')
    for i, quartet in enumerate(iter_pythagore_quartets(2)):
        square = quartet[0][0]**2 + quartet[0][1]**2
        print('{0} = {1[0][0]}² + {1[0][1]}² = {1[1][0]}² + {1[1][1]}²'.format(square, quartet))
        if i == 10:
            break

    print('Smallest integers K so that there exist a,b,c,d,e,f such as K = a² + b² = c² + d² = e² + f² :')
    for i, sixtet in enumerate(iter_pythagore_quartets(3)):
        square = sixtet[0][0]**2 + sixtet[0][1]**2
        print('{0} = {1[0][0]}² + {1[0][1]}² = {1[1][0]}² + {1[1][1]}² = {1[2][0]}² + {1[2][1]}'.format(square, sixtet))
        if i == 10:
            break

if __name__ == '__main__':
    main()

