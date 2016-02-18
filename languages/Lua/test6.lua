#!/usr/bin/lua

print "enter your expression:"
local l = io.read()
local func = assert(loadstring("return " .. l))
print("the value of your expression is " .. func())

-- Essayer : print('Ahaha !') or 0

n = '5'
assert(tonumber(n),
       "invalid input: " .. n .. " is not a number")
