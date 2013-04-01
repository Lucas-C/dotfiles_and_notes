{-
FROM: http://learnyouahaskell.com
-}

f1 = "hello" /= "hello"

one = succ 0

nine = 92 `div` 10 -- same as: div 92 10

doubleUs x y = x*2 + y*2

doubleSmallNumber' x = (if x > 100 then x else x*2) + 1 -- the ' denote a srict version of a function (not lazy)

list = [1,2,3,4] ++ [9,10,11,12] 

woot = ['w','o'] ++ ['o','t'] -- that's string "woot", however ++ can be expensive

cat = 'A':" SMALL CAT" -- "A SMALL CAT" => cheap insertion

-- [1,2,3] is actually just syntactic sugar for 1:2:3:[]

b = "Steve Buscemi" !! 6  -- element access

t1 = [3,2,1] > [2,1,0]
t2 = [3,2] < [2,1,0]
    
h = head [5,4,3,2,1] -- 5 ; the remaining can be obtained with 'tail' ; to get N elements from the beginning : take N [...]
l = last [5,4,3,2,1] -- 1 ; the remaining can be obtained with 'initl' ; to get N elements from the end : drop N [...]

two = length [0,1]
t3 = null []

f2 = elem 0 [1,2,3] -- test if it's an element

alphabet = ['a'..'z'] -- range
infinite = [0,1..] -- infinit range with step

infinite123 = cycle [1,2,3] -- there is also 'repeat oneElem'
threeTens = replicate 3 10 -- [10,10,10]

listComprehension = [ x | x <- [50..100], x `mod` 7 == 3]

length' xs = sum [1 | _ <- xs]

-- ERROR: [(1, "a"), (8, "f", []), (4, "w")]
-- Because list contains only elements of the same type, and the 2nd one here is a different kind of tuple than the 1st

pairs = zip [1..] ["apple", "orange", "cherry", "mango"]
-- [(1,"apple"),(2,"orange"),(3,"cherry"),(4,"mango")]  


