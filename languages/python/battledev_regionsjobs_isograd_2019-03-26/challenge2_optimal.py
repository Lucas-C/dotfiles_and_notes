#!/usr/bin/python3
import sys
def local_print(*args): print(*args, file=sys.stderr)
weights = [0]*101
N = int(input())
for P in range(N):
    weights[int(input())] += 1
count = 0
for first_box in range(100, 0, -1):  # o(9) : iterating all boxes sizes in decreasing order
    while weights[first_box]:  # o(n/9) at worst : while boxes of this size remain, we start a new box
        # boxes = [first_box]
        count += 1
        weights[first_box] -= 1
        remaining_weight = 100 - first_box
        while remaining_weight:  # o(9) at worst : we fill the box at maximum by adding 1st trying to add the biggest boxes
            for box in range(remaining_weight, 0, -1):  # o(9) at worst
                if weights[box]:
                    # boxes.append(box)
                    weights[box] -= 1
                    remaining_weight -= box
                    break
            else:  # not full, but could not find any remaining box to add in it
                break
        # local_print(boxes)
print(count)
