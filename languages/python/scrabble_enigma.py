#!/usr/bin/env python3

# Question que me suis posé : existe-t-il des mots français dont le score au SCRABBLE est unique ?
# Réponse oui, et il n'existe qu'un seul mot au singulier !
# On peut donc en déduire cette énigme :
#    Quel est le seul mot singulier français faisant 57 points au Scrabble ?

# Ce script nécessite une liste de tous les mots de la langue française.
# Pour cela, j'ai employé 2 sources : dl_fr_words.py & https://git.esiee.fr/demphita/tous-les-mots/-/blob/master/mots.txt

A = E = I = L = N = O = R = S = T = U = 1 
D = G = M = 2
B = C = P = 3
F = H = V = 4
J = Q = 8
K = W = X = Y = Z = 10
POINTS = {c: v for c, v in locals().items() if len(c) == 1}
POINTS['-'] = 0

def remove_accents(word):
    word = word                  .replace("Â", "A").replace("À", "A").replace("Ä", "A")
    word = word.replace("É", "E").replace("Ê", "E").replace("È", "E").replace("Ë", "E")
    word = word                  .replace("Î", "I")                  .replace("Ï", "I")
    word = word                  .replace("Ô", "O")                  .replace("Ö", "O")
    word = word                  .replace("Û", "U").replace("Ù", "U").replace("Ü", "U")
    word = word.replace("Ç", "C")
    return word

def score(word):
    total = 0
    for c in word:
        total += POINTS[c]
    return total

with open("mots.txt", encoding="utf-8") as txt_file:
    WORDS = [remove_accents(word.upper()) for word in txt_file.read().splitlines()]
with open("listesdemots.net.txt", encoding="utf-8") as txt_file:
    WORDS += txt_file.read().splitlines()
WORDS = sorted(set(WORDS))

AT_LEAST_TWO = object()  # guard
word_per_score = {}
for word in WORDS:
    s = score(word)
    word_for_score = word_per_score.get(s)
    word_per_score[s] = word if word_for_score is None else AT_LEAST_TWO
print(f"{len(WORDS)} mots traités")
print(f"{len(word_per_score)} scores distincts calculés : {', '.join(map(str, sorted(word_per_score.keys())))}")
for s, word in word_per_score.items():
    if word is not AT_LEAST_TWO:
        print(s, word)

# Output using only https://git.esiee.fr/demphita/tous-les-mots/-/blob/master/mots.txt :
# ( mais ce dictionnaire est incomplet, il ne contient pas par exemple "dodécaèdre" ! )
# 336529 mots traités
# 55 scores distincts calculés : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 57, 58
# 53 psychodysleptiques
# 57 psychophysiologique
# 58 psychophysiologiques

# Output using only https://www.listesdemots.net/touslesmots.htm :
# 416349 mots traités
# 51 scores distincts calculés : 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52
# - Aucun mot unique

# Output using both dictionaries merged:
# 435035 mots traités
# 55 scores distincts calculés : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 57, 58
# 1 A
# 53 PSYCHODYSLEPTIQUES
# 57 PSYCHOPHYSIOLOGIQUE
# 58 PSYCHOPHYSIOLOGIQUES
