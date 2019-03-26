#!/usr/bin/python3
import sys
def local_print(*args): print(*args, file=sys.stderr)
N = int(input())
words = [input() for _ in range(N)]
def all_substrings(word, generated_so_far=None):
    if not generated_so_far:
        generated_so_far = set()
    if len(word) == 2:
        generated_so_far.add(word)
        return generated_so_far
    for i in range(0, len(word)):
        substring = word[:i] + word[i+1:]
        if substring not in generated_so_far:
            generated_so_far.add(substring)
            all_substrings(substring, generated_so_far)
    return generated_so_far
shared_substrings = all_substrings(words[0])
for word in words[1:]:
    substrings = all_substrings(word)
    shared_substrings = {s for s in shared_substrings if s in substrings}
longuest_substring = None
for substring in shared_substrings:
    if not longuest_substring or len(substring) > len(longuest_substring):
        longuest_substring = substring
if longuest_substring:
    print(longuest_substring)
else:
    print('KO')