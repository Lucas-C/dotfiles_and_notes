#!/usr/bin/lua
io.write ("What is your name ? ")
name = io.read ()
print ("Hello " .. name)

-- defines a factorial function
function fact (n)
  if n == 0 then
    return 1
  else
    return n * fact(n-1)
  end
end

print("enter a number:")
a = io.read("*number")        -- read a number
print(fact(a))

