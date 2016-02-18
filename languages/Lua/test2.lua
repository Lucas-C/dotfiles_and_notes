#!/usr/bin/lua

-- store 10 values in a table
a = {}
for i=1,10 do
  a[i] = i^2
end

-- print the lines
print('all content :')
for i,line in ipairs(a) do
  print(line)
end

-- modify the position of the fisrt nil element
a[5] = nil

-- print the lines
print('reduced content :')
for i,line in ipairs(a) do
  print(line)
end


-- Linked list
list = nil
for i=1,10 do
  list = {next=list, value=i}
end

-- skiming
print('linked list :')
l = list
while l do
  print(l.value)
  l = l.next
end


polyline = {color="blue", thickness=2, npoints=4,
             {x=0,   y=0},
             {x=-10, y=0},
             {x=-10, y=1},
             {x=0,   y=1}
           }

print(polyline[2].x)    --> -10

