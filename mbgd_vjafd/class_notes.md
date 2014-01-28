Making Better Group Decisions: Voting, Judgement Aggregation and Fair Division
https://class.coursera.org/votingfairdiv-001

~~~~~~~
~ GOALS:
~ + become a pro-alternative voting system supporter
~ + be able to properly explain current system flaws & alternatives benefits
~~~~~~~


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

### 1-4 -


# Readings
----------
http://rangevoting.org/CompChart.html
http://www.electology.org/electoral-system-summary

### Eric Pacuit, Voting Methods, Stanford Encyclopedia of Philosophy, 2011 (especially sections 1,  2 and 3.1)
