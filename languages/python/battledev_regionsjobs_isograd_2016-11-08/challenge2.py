N = int(input())
for i in range(N):
    stars_count = i*2 + 1 if i <= N // 2 else (N - i - 1)*2 + 1
    margin = (N - stars_count) // 2
    print('.' * margin + '*' * stars_count + '.' * margin)
