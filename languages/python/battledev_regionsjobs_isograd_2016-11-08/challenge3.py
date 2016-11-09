import math
def are_circles_intersecting(c1, c2):
    d = math.sqrt( (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 )
    r, R = min(c1[2], c2[2]), max(c1[2], c2[2])
    return R -r < d < R + r
circles = []
ko = False
N = int(input())
for _ in range(N):
    new_circle = list(map(int, input().split(' ')))
    for circle in circles:
        if are_circles_intersecting(new_circle, circle):
            ko = True
            break
    if ko:
        break
    circles.append(new_circle)
if ko:
    print('KO')
else:
    print('OK')
