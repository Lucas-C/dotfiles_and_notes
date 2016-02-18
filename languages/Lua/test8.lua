#!/usr/bin/lua

function permgen (a, n)
    n = n or table.getn(a)
    if n == 0 then
        coroutine.yield(a)
--~         printResult(a)
    else
        for i=1,n do

            -- put i-th element as the last one
            a[n], a[i] = a[i], a[n]

            -- generate all permutations of the other elements
            permgen(a, n - 1)

            -- restore i-th element
            a[n], a[i] = a[i], a[n]

        end
    end
end
    
function printResult (a)
    for i,v in ipairs(a) do
        io.write(v, " ")
    end
    io.write("\n")
end

--~ permgen ({1,2,3,4})

function perm (a)
    local co = coroutine.create(function () permgen(a) end)
    return function ()     -- iterator
        local code, res = coroutine.resume(co)
        return res
    end
end

function perm (a)
    return coroutine.wrap(function () permgen(a, n) end)
end


for p in perm{"a", "b", "c"} do
    printResult(p)
end

