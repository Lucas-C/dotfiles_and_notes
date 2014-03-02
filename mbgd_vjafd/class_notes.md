Making Better Group Decisions: Voting, Judgement Aggregation and Fair Division
Eric Pacuit
https://class.coursera.org/votingfairdiv-001

~~~~~~~
~ GOALS:
~ + become a pro-alternative voting system supporter
~ + be able to properly explain current system flaws & alternatives benefits
~~~~~~~

Additional readings:
- http://www.votedevaleur.org/co/votedevaleur.html

Voting systems / paradoxes matrix:
- https://en.wikipedia.org/wiki/Voting_system#Compliance_of_selected_systems_.28table.29
- http://eprints.lse.ac.uk/27685/ (include : http://oi57.tinypic.com/2lu2tlh.jpg)


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


### 2-3: Failures of Monotonicity (15:03)

More-is-Less Paradox : Plurality with Runoff

 6  5  4  2
------------
 A  C  B  B  <- swap
 B  A  C  A  <- swap
 C  B  A  C

original result: A wins (2nd column votes are reported to A)
post-swap result: C wins (3rd column votes are reported to C)


No-Show Paradox : Plurality with Runoff (Coombs rule is also sensitive to this paradox)

 4  3  1  3
------------
 A  B  C  C
 B  C  A  B
 C  A  B  A
 ^
 | alt: 2 voters don't show up at the election

original result: C wins (2nd column votes are reported to C)
missing voters result: B wins (1sr column votes a reported to B)
BUT B is ranked over C in the missing voters ballot !

Reverse the point ov view (2 more identical voters), and this is called the Twin Paradox.

Theorem (H. Moulin) : if there are 4 or more candidates, then every Condorcet consistent voting method is susceptible to the No-Show paradox.


### 2-4: Multiple Districts Paradox (12:46)

If a candidate C is the winner in several disjoint electorates, it is possible that, 'ceteris paribus', C will not be elected if the electorates are combined into a single electorate.

Examples: Plurality With Runoff, Majority Judgement

# Simpson's Paradox

A University is hiring in Philosophy & Mathematics. 13 men and 13 women apply for jobs.

              Men   Women
Mathematics   1/5    2/8    Success rate is better for women
Philosophy    6/8    4/5    Success rate is better for women
University    7/13   6/13   Success rate is better for men


### 2-5: Spoiler Candidates and Failures of Independence (9:15)

A candidtae is a **spoiler** if that candidate has little chance of winning, but C's presence in the election draws votes away from candidates that are similar to them, causing a dissimilar candidate to win.

Example: Plurality Rule, Borda Count

Independence of Irrelevant Alternatives: if the voters un two different elec rank 1 and B in exactly the same way, then A and B should be ranked the same way in both elections


### 2-6: Failures of Unanimity (9:46)

If everyone agrees that another candidate is ranked higher than candidate A, then candidate A should not win.

-> Strong Pareto: if there are some people that rank X above Y while all others are indifferent between X and Y, then society ranks X above Y.

Example: Approval Voting (depending on tie rule)

New voting system: successive elimination: serie of rounds where in each of them the candidate with the less votes is eliminated


### 2-7a: Optimal Decisions or Finding a Compromise? (14:27)

It depends if we consider that differences in rankings arise:
- because of erroneous judgements -> how to get the "good" ones ?
- because of differences in values -> how to find a compromise ?

-> need notion of distances between rankings

Kemeny distance: |disagreement on ranking pairs of candidates|

Mean: minimize sum of the squares distances
Median: minimize sum of the absolute distances


### 2-7b: Electing vs. Ranking (9:11)

Kemeny's rule associates a score to each possible linear ordering over the set of candidates:
- a voter contribute to k points to a ranking if his input agrees in k pair-by-pair comparisons
- the Kemeny score of a ranking is the sum of its points over all voters
- the Kemeny ranking is the ranking that maximizes the Kemeny score

Two ways to generate an ordering from a voting method:
- "direct" ordering based on the candidates scores
- "recursive" ordering : winner is ranked 1st, then removed from the election scenario, and we iterate

There is a fundamental incompatibility between electing & ranking.



# Week 3
========

### 3-1: Classifying Voting Methods (8:31)

Main kinds:
- positional scoring rules
- generalized scoring rules
- staged procedures
- Condorcet-guarantee methods

Principles:
- Condorcet: elect the C-winner whenever it exists
- Monotonicity: more support should never hurt a candidate
- Participation: it should never be in a voter's best interests not to vote
- Multiple-Districts: if a candidate wins in each district, then that candidate should also win when the districts are merged.
- Independence: the group's ranking of A and B should only depend ont the voter's ranking of A and Black
- Pareto: never elect a candidate that is dominated
Extras:
- Anonimity
- Neutrality
- Universal Domain : voters are free to rank the candidates in any way they want

Observations:
- Condorcet winner may not exist
- No positional scoring method satisfies the Condorcet Principle
- Condorcet & Participation principles cannot be jointly satisfied


### 3-2a: The Social Choice Model (8:56)

* N is finite set of voters {1,2,3...,n}
* X is a set of alternatives (candidates)
* A relation on X is a linear order if it is transitive, irreflexive and complete (hence, acyclic)
* L(X) is the set of all linear orders over the set XPiY
* O(X) is the set of all reflexive, transitive and complete relations over the set X
* a profile for the set of voters N is a sequence of linear orders over X denoted R = (R1, ..., R2)
* L(X)^n is the set of all profiles for n voters (similarly for O(X)^n)
* For a profile R in O(X)^n, let N_R(A P B) = {i | A P_i B} be the set of voters that rank A above B (similarly for "indifference" N_R(A I B) and N_R(B P I))

Social Welfare Function: F: D -> L(X) where D in L(X)^n

Social Choice Function : SWF: D -> rho(X) -0, we don't care about the final ranking, only the winners


### 3-2b: Anonymity, Neutrality and Unanimity (7:45)

Anonimity: outcome does not depend on the names of the voters
-> For all permutations, for all profiles R in D, F(R) = F(permut(R))

Neutrality: the outcome does not depend on the names of the candidates
-> F(R^perm) = F(R)^perm

Pareto (Unanimity): never elect a candidate that is dominated
-> if N_R(A P B) = N, then A F(R) B


### 3-3: Characterizing Majority Rule (16:53)

When there are only 2 options, can we argue that majority rule is the "best" procedure ?

Unanimity: if v = (v1, ..., vn) with for all i in N, vi = x then F(v) = x (for x in {1,0,-1})
Anonymity: F(v1, ..., vn) = F(v_perm(1), ..., v_perm(n))
Neutrality: F(-v) = -F(v)
Monotonicity (Positive Responsiveness): if F(v) >= 0 and v <karp< v' then F(v') = 1, where v <karp< means for all i in N vi <= vi' and there is some i with vi < vi'

May's Theroem (1952): A social decision method F satisfies unanimity, neutrality, anonymity and monotonicity iff F is majority rule.


### 3-4a: Characterizing Voting Methods (9:42)

Let's model F as a function on |N


### 3-4b: Five Characterization Results (17:44)

1- Positional scoring rules
Let be m the number of candidates, {s1, ..., sm} a set of scores
Npi(j, A) = {i | i ranks A in the jth position}
Score_pi(A) = Sum[j=1,m] sj * |Npi(j,A)|
F is a scoring function if F(pi) = {A | Score(A) >= Score(B) for all B in X}

Theorem[Young]: a social choice correspondence F satisfies anonymity, neutrality, consistency and overwhelming majority iff F is a scoring rule

2- Borda count is a scoring rule with sj = m - j

Theorem[Young]: a social choice correspondence F satisfies anonymity, neutrality, consistency, cancellation and faithfulness iff F is Borda Count.

3- Approval voting

Theorem[Fishburn]: a social choice correspondence F satisfies anonymity, consistency*, cancellation* and faithfulness* iff F is Approval Voting.

4- Plurality rule
...(1996)

5- Range voting
...(2013)


### 3-5: Distance-Based Characterizations of Voting Methods (10:36)

If a profile R is not a consensus profile, then find the closest consensus profile, according to some notion of distance.

Theorem[Nitzan]: The Borda Count winner is the candidate that is the top choice in the closest profile with unanimous top choice, where the distance is measured using the Kemeny distance

cf. 3-5_BordaCountWinner_is_ClosestTopChoiceWithKemenyDist.png


### 3-6: Arrow's Theorem (9:42)

Dictator: society prefers A over B whenever d strictly prefers A over B.

IIA: ( A Ri B <=> A Ri' B ) => ( A F(Ri) B <=> A F(R') B )

Theorem[Arrow, 1951] Suppose that there are at least 3 candidates and finitely many voters. Any social welfare function that satisfies universal domain (voters are free to choose any preference they want), independence of irrelevant alternatives and unanimity is a dictatorship.


### Advanced Lecture: Proof of Arrow's Theorem (30:49)


### 3-7: Variants of Arrow's Theorem (14:35)


### 3-Quizz takeaways
The number of functions from a finite set A to a finite set B is |B|^|A|.

2 candidates, 2 voters:
- there are 3^6 = 729 social welfare functions that satisfy anonymity
- there are 3^2 = 9 social welfare functions that satisfy anonymity and  neutrality
- there are 3 social welfare functions that satisfy anonymity, neutrality and unanimity

Pareto: For any profile P∈O(X)n, if all voters rank A above B, then B∉F(P)
=>
Unanimity: For any profile P∈O(X)n, if for all voters i, top(Pi)=A, then F(P)={A} (recall that for an ordering P, top(P) is the candidate ranked first.)
=>
Non-Imposition: For any candidate A∈X, there is some profile P∈O(X)n such that F(P)={A}

Simple majority means if you get at least half the votes you win, NOT if you get the more votes you win



# Week 4
========

### 4-1: Topics in Social Choice Theory (2:36)

List of Advanced Readings
This week: domain restrictions, strategic voting, Sen's liberal paradox


### 4-2 Domain Restrictions: Single Peakedness (13:42)

- retrict the **domain** pf permissible preferences
- restrict the **distribution** of preferences

"...Maximal disagreement..."
(Q) Could we use a measure of agreement ? So that no candidate/ordering is choosen if there is not enough agreement

Single Peakedness [Duncan Black]: the preferences of group members are said to be single-peaked if the alternatives under consideration can be represented as points on a line and each of the utility functions representing preferences over these alternatives has a maximum at some point on the line and slopes away from this maximum on either side.

Theorem: if there is an odd number of voters that display single-peaked preferences, then a Condorcet winner exists.


### 4-3 Sen's Value Restriction (14:29)

Triplewise value-restriction: for every triple of dictinct candidates A, B, C there exists an xi in {A,B,C} and r in {1,2,3} such that no voter ranks xi has her rth preference among A, B, C

Theorem (Sen, 1966) For every profile satisfying triplewise value-restriction, pairwise majority voting generates a transitive group preference ordering


### 4-4: Strategic Voting (7:02)

- setting the agenda
- misrepresenting preferences


### 4-5a- Defining Strategic Voting (7:40)

Outcome preference for non-singletons:
- weekly dominated
- optimist preference
- pessimist preference
- higher expected utility


### 4-5b: Examples of Manipulation (12:24)

Borda count is single-winner manipulable
Plurality is weak dominance manipulable, but is never single-winner manipulable
Condorcet rule is manipulable by optimists/pessimists, but is never weak cominance manipulable
The Pareto rule is expected utility manipulable, but never manipulable by optimists or pessimists.

Near-unanimity rule: everybody but one (or all) rank a candidate at the top -> it is elected; else: draw.


### Advanced Lecture: Lifting a Preference Relation (19:09)

How do you compare F(R) and F(R ) when they are not singletons?

Given a preference ordering _< over a set of objects X, we want to lift this to an ordering _<^ over a subset rho(X) of X.
Given _<, what reasonable properties can we infer on _<^.


### 4-6: The Gibbard-Satterthwaite Theorem (8:47)

Suppose that X has at least 3 elements. Any resolute social choice function F : L(X)^n -> X that is Pareto and strategy-proof (not manipulable) must be a dictatorship.

Duggan-Schwartz theorem: Suppose that X has at least 3 elements. Any social choice function F : O(X)^n -> (rho(X) - 0) that is non-imposed and cannot be manipulated by an optimist or pessimist has a nominator : i such that for all profiles R, Top(Ri) is in F(R)


### 4-7: Sen's Liberal Paradox (10:14)

Liberalism: for all voters i in N, there exists two alternatives Ai and Bi such that for all profiles R in L(X), if Ai Ri Bi, then B is not in F(R). That is, i decisive over Ai and Bi.

Minimal Liberalism: there are two distincts i and j such that there are alternatives Ai, Bi, Aj and Bj such that i is decisive over Ai and Bi and j is decisive over Aj and Bj.

Sen's Impossibility Theorem: Suppose that X contains at least three elements. No social choice function F: L(X)^n ->  (rho(X) - 0) satisfies universal domain and both minimal liberalism and the Pareto condition.



# Week 5
========

### 5-1: From Preferences to Judgements (4:13)

- group decision with combinatorial structure
- group decision where there is only **one** correct decision and the goal is to find it
- the issues considered are *interconnected*


### 5-2: Anscombe's Paradox (6:26)

        | Issue1 | Issue2 | Issue3
-----------------------------------
voter1  |  Yes   |  Yes   |  No
voter2  |  No    |  No    |  No
voter3  |  No    |  Yes   |  Yes
voter4  |  Yes   |  No    |  Yes
voter5  |  Yes   |  No    |  Yes
MAJORITY|  YES   |  NO    |  YES

A majority of voters do not support the majority outcome on a majority of issues !

Avoiding the paradox: the 3/4 rule:
for each proposal, if the set of voters that agree with the outcome of voting on that proposal is at least three-fourths (whatever the decision method employed), then the set of voters who disagree with the majority of the outcome cannot comprise a majority.

The Ostrogorski paradox:

Candidate A: Issue1=Yes, Issue2=No, Issue3=Yes (majority vote)
Candidate B: Issue1=No, Issue2=Yes, Issue3=No

B gets elected if voters vote for them accordingly to their opinions on issues 1-3 !


### 5-3: Multiple Elections Paradox (6:33)

 YYY YYN YNY YNN NYY NYN NNY NNN
---------------------------------
  1   1   1   3   1   3   3   0

Outcome by majority rule:
Proposition1: N (7-6)
Proposition2: N (7-6)
Proposition3: N (7-6)

But there is no support for NNN !!

 YYYN  YYNY YNYY NYYY NNNN
---------------------------
  2     2    2    2    3

Result: YYYY !!


### 5-4: The Condorcet Jury Theorem (15:58)

A jury need to determine if a defendant is guily or innocent (proposition A).
Each voter i has a probability pi of crorrectly identifying wether A is true or False
Suppose that everyone is "competent" : pi > 0.5

What is the probability that at least m voters are correct ?
\sum_{h=m}^n C(h,n)*p^h*(1-p)^(n-h)

Theorem: Supose Independence & Competence. As the group size increases, the probability that majority opinion is correct increases and converges to one.


### 5-5: Paradoxes of Judgement Aggregation (7:51)

        |   p   | p=>q  |   q
-----------------------------------
expert1 | True  | True  | True
expert2 | True  | False | False
expert3 | False | True  | False
MAJORITY| TRUE  | TRUE  | FALSE

Every expert followed the rules of logic, but the end result does not.

Another example:
p : a valid contract was in place
q : there was a breach of contract
r the court is required to find the defendant liable

  |  p  |  q  | (p&q)<->r |  r
--------------------------------
1 | yes | yes |    yes    | yes
2 | yes | no  |    yes    | no
3 | no  | yes |    yes    | no
M | YES | YES |    YES    | NO

What should be the verdict ?


### 5-6a: The Judgement Aggregation Model (10:15)

Rationality assumptions:
- Ai is logically consistent
- Ai is complete : for each p in the agenda X, either p is in Ai or !p is in Ai

An aggregation function is a map from profiles to judgement sets.

Univeral Domain: the domain of F is the set of all possible profiles of consistent and complete judgement sets

Collective Rationality: F generates consistent and complete collective judgement sets.


### 5-6b: Properties of Aggregation Methods (7:30)

- anonymity
- unanimity
- monotonicity
- systematicity (gather independence + neutrality):
For any p,q in X and all (A1,...,An) and (A1*,...,An*) in the domain of F,
if [for all i in N, p in Ai <=> q in Ai*],
then [p in F(A1,...,An) <=> q in F(A1*,...,An*)]

Theorem[List & Pettit]: if X included in {a,b,a&b}, there exists no aggregation rule satisfying universal domain, collective rationality, systematicity and anonymity.


### 5-7: Impossibility Theorem(s) (9:13)

Def: A set Y is minimally inconsistent if it is inconsistent and every proper subset X included in Y is consistent.

Theorem[Dietrich & List, 2007]: iff an agenda is non-simple and even-number negatable, every aggregation rule satisfying universal domain, collective rationality, systematicity and unanimity is a dictatorship (or inverse dictatorship).

Theorem[Nehring & Puppe, 2002]: iff an agenda is non-simple, every aggregation rule satisfying universal domain, collective rationality, systematicity, unanimity and monotonicity is a dictatorship (or inverse dictatorship).

Theorem[Dietrich & List, 2007]: iff an agenda is totally blocked and even-number negatable, every aggregation rule satisfying universal domain, collective rationality, independence and unanimity is a dactatorship.

Theorem[Nehring & Puppe, 2002,2010]: iff an agenda is totally blocked, every aggregation rule satisfying universal domain, collective rationality, independence, unanimity and monotonicity is a dactatorship.


### 5-Quizz takeaways

Even number of voters may imply non completeness :
p∉Fmaj(A) and ¬p∉Fmaj(A).


