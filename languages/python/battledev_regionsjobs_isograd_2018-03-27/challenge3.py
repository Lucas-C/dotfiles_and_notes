from math import floor
my_notes = list(map(int, input().split()))
N = int(input())
K = int(input())
friends_notes = []
for _ in range(N):
    notes = list(map(int, input().split()))
    match_score = sum(abs(notes[i] - my_notes[i]) for i in range(5))
    friends_notes.append((match_score, notes[5]))
friends_notes = sorted(friends_notes, key=lambda e: e[0])
avg = sum(e[1] for e in friends_notes[:K]) / K
print(floor(avg))