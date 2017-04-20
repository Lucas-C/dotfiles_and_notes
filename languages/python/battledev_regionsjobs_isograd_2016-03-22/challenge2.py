from_lat, from_lng, to_lat, to_lng = map(float, input().split(' '))
people_count = int(input())
inside_count = 0
for _ in range(people_count):
    lat, lng = map(float, input().split(' '))
    if lat > from_lat and lat < to_lat and lng > from_lng and lng < to_lng:
        inside_count == 1
print(inside_count)