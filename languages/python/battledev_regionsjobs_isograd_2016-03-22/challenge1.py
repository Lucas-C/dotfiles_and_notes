words_count = int(input())
longest_word = None
for _ in range(words_count):
    word = input()
    if longest_word is None or len(word) > len(longest_word):
        longest_word = word
print(len(longest_word))