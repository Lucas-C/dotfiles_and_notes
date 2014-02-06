Making Better Group Decisions: Voting, Judgement Aggregation and Fair Division
https://class.coursera.org/votingfairdiv-001

~~~~~~~
~ GOALS:
~ + become a pro-alternative voting system supporter
~ + be able to properly explain current system flaws & alternatives benefits
~~~~~~~

Additional notes:
- http://www.votedevaleur.org/co/votedevaleur.html


# Week 0
========
(total video time: 46:36)

# Readings
----------

### Eric Pacuit, Introduction to Discrete Mathematics,  2013.
https://d396qusza40orc.cloudfront.net/votingfairdiv%2Fdiscretemath.pdf


# Video Lectures
----------------

### 0-1 Relations (8:00)
2nd different definition for an Antisymmetric-relation:
1. for all a,b in A, if aRb and bRa then a=b
2. for all a,b in X, if aRb then not bRa

### 0-2 Representing Preferences (11:39)
[NotePerso] voting is implied to be for a "candidate". So it can be boolean ? What if the vote is to define the value of a speed limit or an age limit ? Are they "continuous candidates" ? What about suggestions polls ? Like "what should we do" ? Is the best approach to request suggestions in a first phase, then close them and vote ?

NOTES:
- prefering X over Y != liking X
- ordinal (simple comparisons) != cardinal (value associated to a vote) information about voters
- voter preferences != ballot he chooses. E.g. when a voter has to fit his preferences onto a linear ordering: or if a voter "strategizes" a ballot

For x,y in X, xR{i}y means that "person {i} prefers x at least as much as y". Then:
- xR{i}y and not yR{i}x : {i} STRONGLY prefer x over y. AKA: xP{i}y
- yR{i}x and not xR{i}y : {i} STRONGLY prefer y over x. AKA: yP{i}x
- xR{i}y and yR{i}x : {i} is INDIFFERENT between x and y. AKA: xI{i}y
- not xR{i}y and not yR{i}x : {i} CANNOT COMPARE x and y.

[NotePerso] This forces a strong model over choices & voting systems.

Rational Preferences Assumptions: comparability (either xPy, yPx or xIy), transitivity, linearity (no xPy)

### 0-3 - Functions (7:31)

### 0-4 - Probability (6:53)

### 0-5 - Propositional Logic (12:33)

Modus Ponens: P, P->Q |- Q
Modus Tollens: !Q, P->Q |- !P
Disjunctive Syllogism: PvQ, !P |- !P
Contraposition: P->Q |- !Q->!P
Monotonicity: if P |- Q, then P,R |- Q

A set of formulas {P1,...,Pn} is INCONSISTENT if there is no valuation V such that
V(Pi) = 1 for all i=1,...,n. A set of formulas is CONSISTENT if it is not inconsistent.



# Week 1
========

# Video Lectures
----------------
(total video time: 1:46:34)

### 1-1 The Voting Problem (14:15)

(debated by de Condorcet & Jean-Charles Bordat)

#voters      3    5    7    6
-------------------------------
 best        A    A    B    C
   ^         B    C    D    B
   |         C    B    C    D
 worst       D    D    A    A

- candidate A should NOT win: more than half rank A last
- candidate D should NOT win: everyone ranks B higher (+ never choosen as 1st choice)
- candidate C: beats every other candidate in head-to-head elelections (Condorcet winner)
- candidate B: has the most "support", taking into account the entire ordering (Borda winner)
Borda scores:
    B: 13 (vs A) + 10 (vs C) + 21 (vs D) = 44
    C: 11 (vs B) + 13 (vs A) + 14 (vs D) = 38
    A: 8 (vs B) + 8 (vs C) + 8 (vs D) = 24
    D: 0 (vs B) + 13 (vs A) + 7 (vs C) = 20


### 1-2 A Quick Introduction to Voting Methods (16:47)

- Plurality Vote: each voter select one candidate
- Borda Count: each voter ranks the candidate on a linear scale starting from 0
- Plurality with Runoff (France): candidates ranking + runoff between top 2 candidates. Sometimes, no runoff if very high initial %vote
- Hare Rule: candidate ranking -> delete candidates with fewest top-vote + iterate
- Coombs Rule: candidate ranking -> delete candidates with most bottom-vote + iterate

#voters      7    5    4    3
-------------------------------
 best        A    B    D    C    # PluralityWithRunoff (and no re-vote) => A wins !!
   ^         B    C    B    D    # Hare Rule => D wins
   |         C    D    C    A    # Coombs Rule => B wins
 worst       D    A    A    B

- Negative voting: allow +1:-1 to candidates
- Approval voting: select a subset of candidates


### 1-3 - Preferences (6:46) == video 0-2


### 1-4 - The Condorcet Paradox (14:55)

N(X P Y) = |{i|XPiY}|
X >=M Y iff N(X P Y) >= N(Y P X)
# >=M is the "group majority relation" or "Condorcer relation"

Condorcet winer X: there is no Y such that Y >=M X
Condorcet looser X: there is no Y such that X >=M Y

Condorcet paradox: >=M is a non-transitive ordering

Example of Condorcet cycle: A >=M B >=M C >=M A

#voters   Voter1  Voter2  Voter3
---------------------------------
            A       C       B
            B       A       C
            C       B       A

Example: split $999 in 3 organizations A, B, C
Motion 1: [$333,$333,$333]
Motion 2: [$499,$499,$1] # A & B ok
Motion 3: [$700, $0, $300] # A & C ok
# Reminds of the "pirates splitting treasure" problem


### Advanced Lecture: How Likely is the Condorcet Paradox? (14:49)

n voters and m candidates

# probability of a Condorcet cycle:
           "number of preferences profiles generating a Cc"
Pr(m,n) = --------------------------------------------------
               "total number of preferences profiles"

total = (m!)^n

... (numerator is problably a count of cycles in a graph)

A Cc looks really likely, assuming a random vote
=> but in reality, the assumption of an "impartial culture" is wrong, and this is a worst case scenario


### 1-5: Condorcet Consistent Voting Methods (11:47)

Majority graph: one vertex per candidate, arrows indicate head-to-head winners

Copeland's rule: the win/loss record for candidate X is WL(X) = |{Y|X >=M Y}| - |{Y|Y >=M X}|.
The Copeland winner is the candidate that maximizes WL.

Black's Rule: the winner Condorcet winner if it exists, else Borda Count winner

Dodgson's Rule: for each candidate, determine the fewest number of pairwise swaps needed to make that candidate the Condorcet winner. The winner is the candidate with the fewest swaps.
# It has many flaws: http://dss.in.tum.de/files/brandt-research/dodgson.pdf

Young method: elect candidates that minimize the number of voters to be removed before they become Condorcet winners


### 1-6: Approval Voting (13:41)

Approval Voting: each voter selects a subset of candidates. The candidate with the most approvals wins.

https://www.youtube.com/watch?v=db6Syys2fmE

Orthogonal informations compared to ranking voting system : they can be deduced from each other.

More flexible than "choose the top N candidates"

Examples of real-life elections that used it:
http://www.nyu.edu/gsas/dept/politics/faculty/brams/theory_to_practice.pdf
-> 6 interesting benefits are listed


### 1-7: Combining Preference and Approval (9:12)


### 1-8: Voting by Grading (14:22)

Questions:
- what grading language (A-F, 0-10, *-****)
- how should we aggregate the grades (avg, median...)
- should there be a "no opinion" option ?

Score Voting / Range voting: the candidate with the largest average grade is declared the winner
http://www.electology.org/score-voting

Majority Voting: the candidate with the largest median grade is declared the winner
Tie-break ? One solution: pick 2nd median grade, then 3rd median...

Dis&Approval voting


### 1-Quizz

A majority candidate is a candidate that is ranked first by more than half of the voters. A voting methods satisfies majority criterion provided it elects the majority candidate (if one exists).

Q6) Every Condorcet consistent voting method satisfies the majority criterion ?
-> True, because a majority candidate beats every other candidate in head-to-head elelections

Q7) If a voting method satisfies the majority criterion, then it is Condorcet consistent.
-> False

Q8) Does the Coombs method satisfy the majority criterion?
-> No, e.g.

 25  26  30  19
----------------
 A   A   ?   ?
 ?   ?   ?   ?
 ?   ?   ?   ?
 B   C   A   D

Q9) Can approval voting elect a Condorcet Loser?
-> Yes, e.g.

 30  30  40
------------
 B   B   C
 *   A   A
 C   *   *
 A   C   B

Q10) Can Score Voting elect a Condorcet Loser?
-> Yes, e.g.

voters  45  55
---------------
  A  |  10  1    <- grades per candidate
  B  |  1   2    <- grades per candidate

Q11) Let P be a relation on X. A cycle is a sequence of elements A1,A2,…,An∈X such that A1PA2P⋯PAnPA1. A relation is acyclic if it does not have a cycle. True or False: If there is a Condorcet winner, then the majority relation is acyclic.
-> False, there can be a cycle between other candidates than the Condorcet winner

Q12) A voting method satisfies the top condition provided a candidate can never be among the winners unless it is ranked first by at least one voter. Select all the voting methods that satisfy the top condition.
- Borda Count : NO, e.g. [E12A]
- The Hare System : YES
- Coombs Rule : NO, e.g. [E12B]

[E12A]: A is the Borda winner
 1  1  1
---------
 B  C  D
 A  A  A
 C  D  B
 D  B  C

[E12B]
 4  2  4
---------
 C  B  B
 A  C  A
 B  A  C


# Readings
----------
http://rangevoting.org/CompChart.html
http://www.electology.org/electoral-system-summary
http://www.rangevoting.org/CondorcetCycles.html

### Eric Pacuit, Voting Methods, Stanford Encyclopedia of Philosophy, 2011 (especially sections 1,  2 and 3.1)



# Week 2
========

### 2-1: Choosing how to Choose (9:15)

Criterias:
- is it easy to use ? (+ is-it even legal ?)
- does it really matter ? I.e. won't all methods produce the same result ?
- information required ? (single choice / measure "intensity")
- axiomatics:
  * Condorcet condition
  * Unanimity: if everyone rank A > B, B should not win
  * Anonymity
  * Monotonicity: a candidate receiving more support shouldn't make her worse off
  * Independence: the winner should not depend on "irrelevant" spoiler candidates
  * Universal Domain: voters are free to rank the candidates in anyway they want


### 2-2a: Condorcet's Other Paradox (7:48)

 2  1  1
---------
 A  C  C
 B  B  A
 C  A  B

Condorcet winner is C, but no scoring system can be used so that C becomes the Borda winner.


### 2-2b: Should we always elect a Condorcet winner? (9:31)

 47  43  5   5
---------------
 A   B   C   C
 C   C   A   B
 B   A   B   A

  C, really ?

 http://rangevoting.org/FishburnAntiC.html
