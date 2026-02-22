#!/usr/bin/lua

f = string.find
a = {"hello", "ll"}

print(f(table.unpack(a)))
