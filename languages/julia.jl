f(x) = x * x
code_llvm(f, (Float64,))
code_native(f, (Float64,))

# 1-based indexing
ismatch(r"^s*#.*$", "# a comment")

h = (x, y) -> x + y
+(1, 2, 3) # operators are functions
fib(n::Int) = n < 2 ? 1 : fib(n - 2) + fib(n - 1) # optional type annotations

type Person
    height::Real
    weight::Real
end

# Matrices
a = [1 2 3; 4 5 6] # 2x3 array
[i * j for i=1:10, j=1:10] # 10x10
b = eye(10, 10) * randn(10, 10)

d = {"name" => "Jack", "id" => 123}

Pkg.available() # return an array of all packages available
Pkg.add("JSON")
using JSON
json(d)
