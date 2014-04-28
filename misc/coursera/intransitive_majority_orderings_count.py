#!/usr/bin/python2.7
"""
A majority ordering for 4 candidates A,B,C,D can be fully determined by 6 boolean values,
characterizing the 6 pairwise comparisons: A vs B, A vs C, A vs D, B vs C, B vs D, C vs D.

(we only need booleans as with an odd number of voters, no equality is possible)

Hence, there are 2^6 = 64 possible orderings for 4 candidates.

For this simulation, lets represent each ordering as a vector of booleans:
    ordering = [compare(A,B), compare(A,C), compare(A,D), compare(B,C), compare(B,D), compare(C,D)]

Then, the transitive ordering A > C > B > D would be [1,1,1,0,1,1].
"""

CANDIDATES = frozenset(('A', 'B', 'C', 'D'))
CANDIDATE_PAIR_TO_ORDERING_INDEX = {
        ('A', 'B') : 0,
        ('A', 'C') : 1,
        ('A', 'D') : 2,
        ('B', 'C') : 3,
        ('B', 'D') : 4,
        ('C', 'D') : 5,
}

def ordering_to_string(ordering):
    comparisons = list(ordering)
    for candidates_pair, index in CANDIDATE_PAIR_TO_ORDERING_INDEX.iteritems():
        comparisons[index] = ('>' if ordering[index] else '<').join(candidates_pair)
    return ' ; '.join(comparisons)

def generate_all_orderings(vector_size):
    if vector_size == 0:
        yield []
        return
    for ordering in generate_all_orderings(vector_size - 1):
        yield [True] + ordering
        yield [False] + ordering

def is_ordering_intransitive(ordering):
    """
    An ordering is intransitive if we can find a cycle in it, starting from any candidate.
    This function uses a greedy method by trying all possible paths that could lead to a cycle.
    """
    for start_candidate in CANDIDATES:
        if find_cycle_in_ordering(ordering, current_candidate=start_candidate, candidates_checked=set()):
            return True
    return False

def find_cycle_in_ordering(ordering, current_candidate, candidates_checked):
    if current_candidate in candidates_checked:
        return True
    candidates_checked.add(current_candidate)
    for challenger_candidate in CANDIDATES:
        if challenger_candidate == current_candidate:
            continue
        if is_candidate_ranked_better(ordering, challenger_candidate, current_candidate):
            if find_cycle_in_ordering(ordering, challenger_candidate, candidates_checked.copy()): # recurse
                return True
    return False

def is_candidate_ranked_better(ordering, candidate1, candidate2):
    """Return True if candidate1 > candidate2 following the ordering"""
    # 'CANDIDATE_PAIR_TO_ORDERING_INDEX' only contains comparisons in one way, e.g. A vs B and not B vs A
    # Hence we need to reverse the logic in the later case
    if candidate1 < candidate2: # this is a nifty trick based on characters ordering
        return ordering[CANDIDATE_PAIR_TO_ORDERING_INDEX[(candidate1, candidate2)]]
    else:
        return not ordering[CANDIDATE_PAIR_TO_ORDERING_INDEX[(candidate2, candidate1)]]

if __name__ == '__main__':
    transitive_orderings = []
    intransitive_orderings = []
    for ordering in generate_all_orderings(vector_size=6):
        if is_ordering_intransitive(ordering):
            intransitive_orderings.append(ordering)
        else:
            transitive_orderings.append(ordering)
    print("There are {} transitive orderings:".format(len(transitive_orderings)))
    print('\n'.join(ordering_to_string(o) for o in transitive_orderings))
    print("There are {} intransitive orderings:".format(len(intransitive_orderings)))
    print('\n'.join(ordering_to_string(o) for o in intransitive_orderings))

