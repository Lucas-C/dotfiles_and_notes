#!/usr/bin/lua

f = string.find
a = {"hello", "ll"}

print(f(unpack(a)))
print(f(a))
