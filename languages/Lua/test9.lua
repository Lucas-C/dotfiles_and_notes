#!/usr/bin/lua

for n in pairs(_G) do print(n) end

print("getmetatable(_G):", getmetatable(_G))


a = 1
local newgt = {}        -- create new environment
setmetatable(newgt, {__index = _G})
setfenv(1, newgt)        -- set it
print(a)                --> 1
