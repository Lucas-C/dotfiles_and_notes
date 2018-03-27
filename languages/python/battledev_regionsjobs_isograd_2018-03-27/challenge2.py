from math import ceil
price = int(input())
N = int(input())
total = 0
for _ in range(N):
    people_count = int(input())
    if people_count >= 10:
        total += .7 * price * people_count
    elif people_count >= 6:
        total += .8 * price * people_count
    elif people_count >= 4:
        total += .9 * price * people_count
    else:
        total += price * people_count
print(ceil(total))