#!/usr/bin/python2.7
from math import factorial
import string
from itertools import combinations

def build_candidate_pair_to_ordering_index(candidates):
    candidate_pair_to_ordering_index = {}
    for i, c in enumerate(combinations(candidates, 2)):
        candidate_pair_to_ordering_index[c] = i
    return candidate_pair_to_ordering_index

def generate_all_orderings(vector_size):
    if vector_size == 0:
        yield []
        return
    for ordering in generate_all_orderings(vector_size - 1):
        yield [True] + ordering
        yield [False] + ordering

def count_intransitive_orderings(candidates_count):
    candidates = string.ascii_uppercase[:candidates_count]
    candidate_pair_to_ordering_index = build_candidate_pair_to_ordering_index(candidates)

    def ordering_to_string(ordering):
        comparisons = list(ordering)
        for candidates_pair, index in candidate_pair_to_ordering_index.iteritems():
            comparisons[index] = ('>' if ordering[index] else '<').join(candidates_pair)
        return ' ; '.join(comparisons)

    def is_ordering_intransitive(ordering):
        """
        An ordering is intransitive if we can find a cycle in it, starting from any candidate.
        This function uses a greedy method by trying all possible paths that could lead to a cycle.
        """
        for start_candidate in candidates:
            if find_cycle_in_ordering(ordering, current_candidate=start_candidate, candidates_checked=set()):
                return True
        return False

    def find_cycle_in_ordering(ordering, current_candidate, candidates_checked):
        if current_candidate in candidates_checked:
            return True
        candidates_checked.add(current_candidate)
        for challenger_candidate in candidates:
            if challenger_candidate == current_candidate:
                continue
            if is_candidate_ranked_better(ordering, challenger_candidate, current_candidate):
                if find_cycle_in_ordering(ordering, challenger_candidate, candidates_checked.copy()): # recurse
                    return True
        return False

    def is_candidate_ranked_better(ordering, candidate1, candidate2):
        """Return True if candidate1 > candidate2 following the ordering"""
        # 'candidates, candidate_pair_to_ordering_index' only contains comparisons in one way, e.g. A vs B and not B vs A
        # Hence we need to reverse the logic in the later case
        if candidate1 < candidate2: # this is a nifty trick based on characters ordering
            return ordering[candidate_pair_to_ordering_index[(candidate1, candidate2)]]
        else:
            return not ordering[candidate_pair_to_ordering_index[(candidate2, candidate1)]]

    ordering_vector_size = len(candidate_pair_to_ordering_index)
    orderings_count = 2 ** ordering_vector_size
    intransitive_orderings_count = 0
    for ordering in generate_all_orderings(ordering_vector_size):
        if is_ordering_intransitive(ordering):
            intransitive_orderings_count += 1
    return intransitive_orderings_count, orderings_count
 
if __name__ == '__main__':
    for candidates_count in xrange(3,8):
        intransitive_orderings_count, orderings_count = count_intransitive_orderings(candidates_count)
        assert intransitive_orderings_count == orderings_count - factorial(candidates_count) 
        intransitive_orderings_proportion = float(intransitive_orderings_count) / orderings_count
        print(candidates_count, intransitive_orderings_count, intransitive_orderings_proportion)
