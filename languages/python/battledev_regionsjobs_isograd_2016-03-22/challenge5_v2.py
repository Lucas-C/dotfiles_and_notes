def debug(*args):
    try:
        local_print(' '.join(map(str, args)))
    except NameError:
        import sys; print(*args, file=sys.stderr)

N = int(input())
debug(N)
heights = [int(input()) for _ in range(N)]
length = 0
for i in range(N):
    height = heights[i]
    j = i + 1
    while j < N and heights[j] <= height:
        if heights[j] == height:
            length += j - i
            break
        j += 1
print(length) # Maximum execution time has been reached !!