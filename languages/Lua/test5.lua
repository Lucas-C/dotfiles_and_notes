#!/usr/bin/lua

-- Illustrate external local variable ALIAS upvalue

function newCounter ()
  local i = 0
  return function ()   -- anonymous function
           i = i + 1
           return i
         end
end

c1 = newCounter()
print(c1())  --> 1
print(c1())  --> 2

c2 = newCounter()
print(c2())  --> 1
print(c1())  --> 3
print(c2())  --> 2
