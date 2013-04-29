{-
FROM: http://learnyouahaskell.com
ghci:
    :l file.hs                          -- load file
    :r                                  -- reload
    :t func                             -- get type
    :m + Data.List Data.Map Data.Set    -- load modules
-}

import Data.List (nub) -- cf. Loading Modules, all imports MUST be done before code start
import Data.List hiding (nub)
import qualified Data.Map as M

{-############
# Starting Out
  ############-}

f1 = "hello" /= "hello"

one = succ 0

nine = 92 `div` 10 -- same as: div 92 10

doubleUs x y = x*2 + y*2

doubleSmallNumber' x = (if x > 100 then x else x*2) + 1 -- the ' denote a srict version of a function (not lazy)

list = [1,2,3,4] ++ [9,10,11,12] 

woot = ['w','o'] ++ ['o','t'] -- that's string "woot", however ++ can be expensive

scat = 'A':" SMALL CAT" -- "A SMALL CAT" => cheap insertion

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


{-###################
# Types & Typeclasses
  ###################-}

-- 1 object tuple == object

-- ERROR: [(1, "a"), (8, "f", []), (4, "w")]
-- Because list contains only elements of the same type, and the 2nd one here is a different kind of tuple than the 1st

pairs = zip [1..] ["apple", "orange", "cherry", "mango"]
-- [(1,"apple"),(2,"orange"),(3,"cherry"),(4,"mango")]  

-- Primitive types : Int, Integer -- unbounded, Float, Double, Bool, Char, String == [Char]

-- Type variables: a, b, c...
-- Class contraints : =>
-- :t (==)
-- (==) :: (Eq a) => a -> a -> Bool

-- Eq
f3 = "Ho Ho" /= "Ho Ho"

-- Ord
lt = "Abrakadabra" `compare` "Zebra"

-- Show
string = show 3

-- Read
rl = read "[1,2,3,4]" :: [Int] -- type annotation needed as there is no implicit conversion

-- Enum
zero = succ (-1)
abcde = ['a'..'e']

-- Bounded : Int; Char, Bool

-- Num
-- Integral
-- Floating


{-###################
# Syntax in functions
  ###################-}

sayMe :: (Integral a) => a -> String  
sayMe 1 = "One!"  
sayMe 2 = "Two!"  
sayMe 3 = "Three!"  
sayMe x = "Not between 1 and 3"
sayMe 4 = "Will never match"

addVectors :: (Num a) => (a, a) -> (a, a) -> (a, a)  
addVectors (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)  

xs = [(1,3), (4,3), (2,4), (5,3), (5,6), (3,1)]
sum_xs = [a+b | (a,b) <- xs]  -- pattern matching with list comprehensions

head' :: [a] -> a  
head' [] = error "Can't call head on an empty list, dummy!"  
head' (x:_) = x

tell :: (Show a) => [a] -> String
tell [] = "The list is empty"  
tell (x:[]) = "The list has one element: " ++ show x  
tell (x:y:[]) = "The list has two elements: " ++ show x ++ " and " ++ show y  
tell (x:y:_) = "This list is long. The first two elements are: " ++ show x ++ " and " ++ show y 

bmiTell :: (RealFloat a) => a -> a -> String  
bmiTell weight height  
    | bmi <= 18.5 = "You're underweight, you emo, you!"  
    | bmi <= 25.0 = "You're supposedly normal. Pffft, I bet you're ugly!"  
    | bmi <= 30.0 = "You're fat! Lose some weight, fatty!"  
    | otherwise   = "You're a whale, congratulations!"  
    where bmi = weight / height ^ 2  

myCompare :: (Ord a) => a -> a -> Ordering  
a `myCompare` b  
    | a > b     = GT  
    | a == b    = EQ  
    | otherwise = LT  

six00 = (let (a,b,c) = (1,2,3) in a+b+c) * 100  

fatBMI xs = [bmi | (w, h) <- xs, let bmi = w / h ^ 2, bmi >= 25.0] 

describeList :: [a] -> String  
describeList xs = "The list is " ++ case xs of [] -> "empty."  
                                               [x] -> "a singleton list."   
                                               xs -> "a longer list."  


{-#########
# Recursion 
  #########-}

quicksort :: (Ord a) => [a] -> [a]  
quicksort [] = []  
quicksort (x:xs) =   
    let smallerSorted = quicksort [a | a <- xs, a <= x] 
        biggerSorted = quicksort [a | a <- xs, a > x]  
    in  smallerSorted ++ [x] ++ biggerSorted  


{-######################
# Higher order functions 
  ######################-}

divideByTen :: (Floating a) => a -> a
divideByTen = (/10)

isUpperAlphanum :: Char -> Bool
isUpperAlphanum = (`elem` ['A'..'Z'])

applyTwice :: (a -> a) -> a -> a 
applyTwice f x = f (f x)

-- zipWith
evenTo10 = zipWith (*) (replicate 5 2) [1..]

-- flip
pairs2 = flip zip [1,2,3,4,5] "hello"

-- map
onomatop = map (++ "!") ["BIFF", "BANG", "POW"] 

-- filter
filtered = filter (`elem` ['A'..'Z']) "i lauGh At You BecAuse u r aLL the Same"

-- takeWhile
sumOddSquareSmallerThan x = sum (takeWhile (<x) (filter odd (map (^2) [1..])))

collatz :: (Integral a) => a -> [a]
collatz 1 = [1]
collatz n
    | even n =  n:collatz (n `div` 2)
    | odd n  =  n:collatz (n*3 + 1)

-- lambdas
numLongChains = length (filter (\xs -> length xs > 15) (map collatz [1..100]))

-- foldl / foldr / foldl1 / foldr1
-- strict versions (non-lazy) : foldl' & foldl1' from Data.List
sum' :: (Num a) => [a] -> a
sum' = foldl1 (+)

elem' :: (Eq a) => a -> [a] -> Bool  
elem' y ys = foldl (\acc x -> if x == y then True else acc) False ys 

-- scanl / scanr / scanl1 / scanr1 : same bur return q list of the successive accumulators

-- $ == application : f $ g $ z x == f( g( z(x) ) )
app = map ($ 3) [(4+), (10*), (^2), sqrt]

-- . == composition : (f . g . z) x == f( g( z(x) ) )


{-###############
# Loading modules 
  ###############-}

numUniques :: (Eq a) => [a] -> Int 
numUniques = length . nub

-- http://www.haskell.org/ghc/docs/latest/html/libraries/
-- http://www.haskell.org/hoogle/

sigle = intersperse '.' "MONKEY"
spaced = intercalate " " ["hey","there","guys"] 
tr = transpose [[0,0,0],[1,1,1],[2,2,2]]
cat = concat ["c","a","t"]

sup4 = and $ map (>4) [5,6,7,8]
nosup4 = or $ map (>4) [1,2,3]
inf4 = all (<4) [1,2,3]
noinf4 = any (<4) [5,6,7,8]

power2 = take 10 $ iterate (*2) 1
appeal = splitAt 3 "heyman"

