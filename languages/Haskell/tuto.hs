{-
FROM: http://learnyouahaskell.com
$ ghci:
    :l file.hs                          -- load file
    :r                                  -- reload
    :t func                             -- get type
    :k                                  -- get kind (meta-type)
    :m + Data.List Data.Map Data.Set    -- load modules
    :cd e:\code
    :module                                -- "set the context for expression evaluation"
    :info <whatever>

$ ghc-pkg list

$ hoogle "Num a => [a] -> a"
$ hlint

Shell one-liners helpful tools:
    hrunl () { ghc -e "interact(show.($*).lines)"; }
    hrunw () { ghc -e "interact(show.($*).words)"; }
    hrunwl () { ghc -e "interact(show.($*).map words.lines)"; }
E.g:
    $ find -maxdepth 1 -type f | xargs du | hrunwl "sum . map (read . head)"
-}

-- All imports MUST be done before code start
-- 2 first following forms preferred
import qualified Data.Map as Map
import qualified Data.Set as Set
import Data.Function (on)
import Control.Monad (forever, forM)
import Data.List hiding (unzip7)
import Data.List
import Data.Char
import Module.Mod
import System.IO
import System.Random -- need libghc-random-dev
import qualified Data.ByteString as BS
import qualified Data.ByteString.Lazy as BSL -- -> 64K chunks
import System.Environment
import Control.Exception
import System.IO.Error
import Control.Applicative
import Data.Monoid
import Control.Monad
import Data.Ratio

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

uppercaseB = "Steve Buscemi" !! 6  -- element access

t1 = [3,2,1] > [2,1,0]
t2 = [3,2] < [2,1,0]

h = head [5,4,3,2,1] -- 5 ; the remaining can be obtained with 'tail' ; to get N elements from the beginning : take N [...]
l = last [5,4,3,2,1] -- 1 ; the remaining can be obtained with 'initl' ; to get N elements from the end : drop N [...]

two = length [0,1]
t3 = null []

f2 = elem 0 [1,2,3] -- test if it's an elementi ; opposite: notElem
-- also: elemIndex, elemIndices : return indices or Nothing

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

pairs = zip [1..] ["apple", "orange", "cherry", "mango"] -- also: zip3, zip4...
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
-- 'reads' more robust if input invalid

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
eveni_to10 = zipWith (*) (replicate 5 2) [1..]
-- also: zipWith3, zipWith4...

-- flip
pairs2 = flip zip [1,2,3,4,5] "hello"

-- map
onomatop = map (++ "!") ["BIFF", "BANG", "POW"]

-- filter
filtered = filter (`elem` ['A'..'Z']) "i lauGh At You BecAuse u r aLL the Same"

-- takeWhile
sum_oddS_square_smaller_than x = sum (takeWhile (<x) (filter odd (map (^2) [1..])))

collatz :: (Integral a) => a -> [a]
collatz 1 = [1]
collatz n
    | even n =  n:collatz (n `div` 2)
    | odd n  =  n:collatz (n*3 + 1)

-- lambdas
num_long_chains = length (filter (\xs -> length xs > 15) (map collatz [1..100]))

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

-- http://learnyouahaskell.com/modules#loading-modules
-- http://www.haskell.org/ghc/docs/latest/html/libraries/
-- http://www.haskell.org/hoogle/

-- # Data.List #

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
magritte = dropWhile (/=' ') "This is a pipe"

part = partition (>3) [1,3,5,6,3,2,1,0,3,7]
-- Also: break <predicate> <=> span (not . <predicate>)

sorted = sort [2,4,1,3]

t4 = "pref" `isPrefixOf` "prefix"
t5 = "ix" `isSuffixOf` "suffix"

just4 = find (>4) [1,2,3,4,5,6]
-- also: findIndex, findIndices

splitted_lines = lines "first line\nsecond line\nthird line" -- reverse: unlines

del = delete 'h' "hey there ghang!"

set_diff = [1..10] \\ [2,5,9]
set_union = [1..7] `union` [5..10]
set_intersect = [1..7] `intersect` [5..10]

insert_keeping_stuff_sorted = insert 4 [3,5,1,2,8,2]

-- Generic equivalents:
-- genericLength, genericTake, genericDrop, genericSplitAt, genericIndex, genericReplicate
-- nubBy, deleteBy, unionBy, intersectBy, groupBy

values = [-4.3, -2.4, -1.2, 0.4, 2.3, 5.9, 10.5, 29.1, 5.3, -2.4, -14.5, 2.9, 2.3]
grouped_by_sign = groupBy ((==) `on` (> 0)) values

-- # Data.Char #

categories_examples = map generalCategory " \t\nA9?|"

ascii_values = map ord ['a'..'z'] -- reverse: chr

-- # Data.Map #

dict = Map.fromList [("lucas", 42),("laetitia", 127)] -- reverse: toList

m = Map.insert 3 100 Map.empty
f4 = Map.null m
toto = Map.size m
answer = Map.lookup "lucas" dict

-- map, filter
-- keys, elems
-- fromListWith, insertWith

-- # Data.Set #

text1 = "I just had an anime dream. Anime... Reality... Are they so different?"
text2 = "The old man left his garbage can out and now his trash is all over my lawn!"

set1 = Set.fromList text1
set2 = Set.fromList text2

i1_2 = Set.intersection set1 set2
u1_2 = Set.union set1 set2
d1_2 = Set.difference set1 set2

-- null, size, member, empty, singleton, insert, delete
-- map, filter

setNub xs = Set.toList $ Set.fromList xs
-- "setNub is generally faster than nub on big lists but nub preserves the ordering of the list's elements, while setNub does not."


{-####################################
# Making Our Own Types and Typeclasses
  ####################################-}

data Shape = Circle Float Float Float | Rectangle Float Float Float Float deriving (Show)
-- Circle, Rectangle : value constructors

surface :: Shape -> Float
surface (Circle _ _ r) = pi * r ^ 2
surface (Rectangle x1 y1 x2 y2) = (abs $ x2 - x1) * (abs $ y2 - y1)

-- module Shapes
-- ( Shape(..), --> the 2 dots indicate that ALL value constructors are exported, same as "Shape(Rectangle, Circle)" here

data Person = Person { firstName :: String
                     , lastName :: String
                     , age :: Int
                     , height :: Float
                     , phoneNumber :: String
                     , flavor :: String
                     } deriving (Show)
-- Haskell automatically create the functions on the right to consult the fields

-- data Bool = False | True
-- data Maybe a = Nothing | Just a  -- TYPE constructor

-- deriving (Eq, Ord...)
-- For Ord: the value which was made with a constructor that's defined first is considered smaller
-- For Enum: all value constructors are nullary (take no parameters, i.e. fields)

type Name = String -- type synonym
type AssocList k v = [(k,v)] -- parametrized type synonym

-- data Either a b = Left a | Right b deriving (Eq, Ord, Read, Show)


-- Redifining lists !
infixr 5 :-:  -- '5' is the 'fixity'
-- "We can define functions to be automatically infix by making them comprised of only special characters."
data List a = Empty | a :-: (List a) deriving (Show, Read, Eq, Ord)

infixr 5 .++
(.++) :: List a -> List a -> List a
Empty .++ ys = ys
(x :-: xs) .++ ys = x :-: (xs .++ ys)

a = 3 :-: 4 :-: 5 :-: Empty
b = 6 :-: 7 :-: Empty
a_b = a .++ b


-- Binary search tree
data Tree a = EmptyTree | Node a (Tree a) (Tree a) deriving (Show, Read, Eq)

singleton :: a -> Tree a
singleton x = Node x EmptyTree EmptyTree

treeInsert :: (Ord a) => a -> Tree a -> Tree a
treeInsert x EmptyTree = singleton x
treeInsert x (Node a left right)
    | x == a = Node x left right
    | x < a  = Node a (treeInsert x left) right
    | x > a  = Node a left (treeInsert x right)

treeElem :: (Ord a) => a -> Tree a -> Bool
treeElem x EmptyTree = False
treeElem x (Node a left right)
    | x == a = True
    | x < a  = treeElem x left
    | x > a  = treeElem x right

nums = [8,6,4,1,7,3,5]
numsTree = foldr treeInsert EmptyTree nums

-- TYPECLASSES
-- class Eq a where
--    (==) :: a -> a -> Bool
--    (/=) :: a -> a -> Bool
--    x == y = not (x /= y)
--    x /= y = not (x == y)

data TrafficLight = Red | Yellow | Green

instance Eq TrafficLight where
    Red == Red = True
    Green == Green = True
    Yellow == Yellow = True
    _ == _ = False

instance Show TrafficLight where
    show Red = "Red light"
    show Yellow = "Yellow light"
    show Green = "Green light"


-- class Functor f where
--     fmap :: (a -> b) -> f a -> f b


{-###############
# Input & Output
  ###############-}

-- $ ghc --make helloworld && ./helloworld
-- $ runhaskell helloworld.hs

-- BEWARE 'return' : it just makes an I/O action out of a pure value

-- putStr, putChar
-- print (~ putStrLn . show)
-- getChar

listOfIO = map print nums
printNums = do results <- sequence listOfIO ; return results

-- 'mapM nums' is an equivalent as it maps a function that returns an I/O action over a list and then sequence it
-- to discard result, use mapM_
myMapM1 a b = sequence (map a b)
myMapM2 f = sequence . map f

getAndPrintLine = do s <- getLine ; putStrLn s
echo = forever getAndPrintLine -- repeat IO action forever

read2Lines = do reslist <- forM [1,2] (\i -> do e <- getLine ; return e) ; return reslist
-- forM is like mapM with reversed parameters
-- (\a -> do ... ) is a function that takes a number and returns an I/O action

-- getCOntents: lazy I/O action that reads everything from the standard input until it encounters an end-of-file character
-- interact: takes a function of type String -> String as a parameter and returns an I/O action that will take some input,
--      run that function on it and then print out the function's result

-- # Files IO #
-- openFile :: FilePath -> IOMode -> IO Handle
-- type FilePath = String
-- data IOMode = ReadMode | WriteMode | AppendMode | ReadWriteMod
-- hClose :: Handle -> IO ()

printTestFile = do
    withFile "test_file.txt" ReadMode (\handle -> do
        contents <- hGetContents handle
        putStr contents)

-- hGetLine, hPutStr, hPutStrLn, hGetChar
-- readFile, writeFile, appendFile
-- hSetBuffering; hFlush
-- openTempFile, renameFile, removeFile
-- getArgs, getProgName

-- # Randomness #
-- random :: (RandomGen g, Random a) => g -> (a, g)
r = random (mkStdGen 100) :: (Int, StdGen)
r5 = take 5 $ randoms (mkStdGen 11) :: [Float]
rPswd = take 10 $ randomRs ('a','z') (mkStdGen 42)
getIOGen = do getStdGen -- !! Same generator returned if called twice in the same program invocation, use newStdGen

-- # Bytestrings #
lc_letters = BSL.pack [97..122] -- reverse: unpack
-- fromChunks / toChunks : conversion strict/lazy BS
strict_bs = foldr BS.cons BS.empty [50..60]
lazy_bs = foldr BSL.cons BSL.empty [50..60]
lazy_bs_with_strict_cons = foldr BSL.cons' BSL.empty [50..60]
-- Available functions: head, tail, init, null, length, map, reverse, foldl, foldr, concat, takeWhile, filter
-- readFile

-- # Exceptions #
-- "Pure code can throw exceptions, but it they can only be caught in the I/O part"
-- catch :: IO a -> (IOError -> IO a) -> IO a
contents = readDumbFile `catch` handler
readDumbFile = do contents <- readFile "dumb_file.txt" ; putStrLn contents
handler e
    | isDoesNotExistError e =
        case ioeGetFileName e of Just path -> putStrLn $ "Whoops! File does not exist at: " ++ path
                                 Nothing -> putStrLn "Whoops! File does not exist at unknown location!"
    | otherwise = ioError e
-- Also: isAlreadyExistsError, isDoesNotExistError, isAlreadyInUseError, isFullError, isEOFError, isIllegalOperation, isPermissionError, isUserError


{-##########################################
# Functors, Applicative Functors and Monoids
  ##########################################-}

-- # Functors #
revGetLine = do fmap reverse getLine
-- Functor laws:
--  - fmap id = id
--  - fmap (f . g) = fmap f . fmap g

-- # Applicative Functors #
--   instance Applicative Maybe where
--       pure = Just
--       Nothing <*> _ = Nothing
--       (Just f) <*> something = fmap f something

j12 = Just (+3) <*> Just 9
nope = Nothing <*> Just "woot"
j8 = pure (+) <*> Just 3 <*> Just 5

actor = (++) <$> Just "johntra" <*> Just "volta"
list_comp = (*) <$> [2,5,10] <*> [8,10,11] -- [ x*y | x <- [2,5,10], y <- [8,10,11]]

size8list = [(+),(*)] <*> [1,2] <*> [3,4]

res508 = (+) <$> (+3) <*> (*100) $ 5

zipl = getZipList $ (+) <$> ZipList [1,2,3] <*> ZipList [100,100..]

-- Applicative Functors Laws
--  - pure id <*> v = v
--  - pure (.) <*> u <*> v <*> w = u <*> (v <*> w)
--  - pure f <*> pure x = pure (f x)
--  - u <*> pure y = pure ($ y) <*> u

-- # newtype #
newtype CharList = CharList { getCharList :: [Char] } deriving (Eq, Show)
-- faster & lazier than 'data'

-- # Monoids #
-- mempty, mappend, mconcat
-- Sum, Product
-- Any, All

-- import Data.Foldable


{-###################
# A Fistful of Monads
  ###################-}
-- 'bind': (>>=) :: (Monad m) => m a -> (a -> m b) -> m b
-- If we have a fancy value and a function that takes a normal value
-- but returns a fancy value, how do we feed that fancy value into the function?

-- '>>' acts as '>>= \_ ->' : its systematically return its right hand side
-- 'fail'
wopwop = do (x:xs) <- Just "" ; return x

-- The MonadPlus type class is for monads that can also act as monoids

weird_cond = guard (1 > 2) >> return "cool" :: Maybe String

-- Monad laws:
--  - return x >>= f is the same damn thing as f x
--  - m >>= return is no different than just m
--  - (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)


{-#####################
# For a Few Monads More
  #####################-}
-- # Writer #

-- # DiffList #
newtype DiffList a = DiffList { getDiffList :: [a] -> [a] }

toDiffList :: [a] -> DiffList a
toDiffList xs = DiffList (xs++)

fromDiffList :: DiffList a -> [a]
fromDiffList (DiffList f) = f []

instance Monoid (DiffList a) where
    mempty = DiffList (\xs -> [] ++ xs)
    (DiffList f) `mappend` (DiffList g) = DiffList (\xs -> f (g xs))

-- # State monad #
-- s -> (a,s) 

-- # Monadic functions #
-- liftM :: (Monad m) => (a -> b) -> m a -> m b -- Equivalent to 'fmap' 
-- ap :: (Monad m) => m (a -> b) -> m a -> m b  -- Equivalent to '<*>'
-- liftM2 :: (Monad m) => (a -> b -> c) -> m a -> m b -> m c -- Equivalent to 'liftA2'

-- join :: (Monad m) => m (m a) -> m a -- flaten nested monadic value
-- filterM :: (Monad m) => (a -> m Bool) -> [a] -> m [a]
-- foldM :: (Monad m) => (a -> b -> m a) -> a -> [b] -> m a

-- # Rationals #
frac = 1%3 + 5%4


{-##################
# Random other notes
  ##################-}
-- | Left-to-right Kleisli composition of monads.
(>=>)       :: Monad m => (a -> m b) -> (b -> m c) -> (a -> m c)
f >=> g     = \x -> f x >>= g

-- (a ? b $ c)  ==  (if a then b else c)
True ? x = const x
False ? _ = id

absurd = let 1=2 in print "[head explodes]"
