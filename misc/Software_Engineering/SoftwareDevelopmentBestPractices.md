## References
- [CC-\\w\\d+] : Clean Code - Robert C. Martin - Ed. Prentice Hall
- [PP] : The Pragmatic Programmer - Andrew Hunt & David Thomas - Ed. Addison-Wesley
- [AOSA] : [The Architecture of Open Source Applications](http://www.aosabook.org) - Amy Brown & Greg Wilson
- [JP] : Java Puzzlers - Joshua Bloch & Neal Gafter - Ed. Addison-Wesley
- [SDP] : [Software Design Philosophy - John Ousterhout](https://ramcloud.stanford.edu/wiki/display/ramcloud/Software+Design+Philosophy)
- [97TEPSK] : [97 Things Every Programmer Should Know](http://programmer.97things.oreilly.com/wiki/index.php/Contributions_Appearing_in_the_Book)
- [DOM] : [Don't overuse mocks](http://googletesting.blogspot.com/2013/05/testing-on-toilet-dont-overuse-mocks.html)
- [KYTD] : [Know your test doubles](http://googletesting.blogspot.com/2013/07/testing-on-toilet-know-your-test-doubles.html)
- [CRoTDD] : [CR over TDD](http://svenpet.com/2014/01/07/better-code-reviews/)
- [JC-PI] : [John Carmack on Parallel Implementations](http://www.altdev.co/2011/11/22/parallel-implementations/)
- [RobPikeKenThompson] : [What Rob Pike learned from KenThompson](http://www.informit.com/articles/article.aspx?p=1941206)

My rule #1 : Follow standard conventions within a team [CC-G24]

## Main "mantras"
- Boy Scout Rule & Broken Window Theory
- KISS & YAGNI : Keep It Simple, Stupid & You Aren't Gonna Need It
- Duplication : DRY ! Once, and only once. [CC-G5]
    switch/case OR if/else chain -> polymorphism if appears more than once [CC-G23]
    similar algorithm            -> template method / strategy pattern
- "Premature optimization is the root of all evil"
- Code Fearlessly & implement alternative code versions in parallel [JC-PP]

## Design principles 
where "Design" = Organisation of the software logic

SE = software entity : class, module, function...

- Single Responsability Principle : every SE should have a single responsibility, and that responsibility should be entirely encapsulated by the SE
- Law of Demeter : each SE should have only limited knowledge about other SEs. Write "shy code". Talk to friends; Don’t talk to strangers [CC-G36]
- Open/Closed Principle : SE should be open for extension, but closed for modification
- Common Closure Principle : any change to the software should only have a very local impact

## Design smells
- "Thin" classes. Ideally, a class should have a very simple interface that hides a lot of functionality and internal complexity. [SDP]
    Too much information : hide you data, hide your utility functions, hide your constants & temporaries, concentrate on keeping small interfaces to keep coupling low [CC-G8]
- Code at wrong level of abstraction : e.g. functions should descend only one level of abstraction [CC-G6] [CC-G34]
- Classes designed around algorithms or time order (i.e. collect all the things that happen at one point in time into a single class) : design classes around INFORMATION [SDP]
    "It is almost always incorrect to begin the decomposition of a system into modules on the basis of a flowchart. We propose instead that one begins with a list of difficult design decisions or design decisions which are likely to change." - On the criteria to be used in decomposing systems into modules, D. Parnas
- Base classes depending on their derivatives [CC-G7]
- Logical dependencies are not physical : avoid assumptions on other modules behaviour, make it explicit + expose objects modifications (functional programing) [CC-G22] [CC-G31]
- Artifical coupling / Misplaced responsability [CC-G13] [CC-G14] [CC-G17]
    There is a place for everything : don't toss code in the most convenient place at hand, take the time to figure out where functions, constants, variables ought to be declared
- when in doubt, favor composition over inheritance [JP-C6]

## Be rigorous and clean after yourself
- Be consistent : be careful with the conventions you choose, and follow them strictly. E.g. stick with one word per concept. [CC-G11]
- Structure over convention : e.g. base clase enforce interface whereas switch/case can contain anything [CC-G27]
- Don't override safeties : e.g. turning off compiler warnings or some failing tests. Think about Chernobyl ! [CC-G4]
- Remove dead code : unused function, impossible "if" condition, useless try/catch... [CC-F4] [CC-G9] [CC-G12]

## Code intent should be obvious
- Understand the algorithm first [CC-G21]
- Don't be arbitrary, you must be able to justify any decision in your code [CC-G32]
- Use explanatory variables [CC-G19]
- Replace magic numbers with named constants + try to gather configuration [CC-G25]
- Conditionals : encapsulate them instead of making and/or combinations inline, avoid double negation [CC-G28] [CC-29]
- Obscured intent : in doubt, detail your motivation as comments [CC-G16]

## Code formatting
- Keep source files short !
- Write top-down code that reads like a narrative [CC-Chapt2]
- Vertical separation : define things close to where they are used [CC-G10]
- Do not line up variable names in a set of declarations/assignement statements [CC-Chapt5]
- keep lines length short (~80char) because it keeps the code readable + one can view multiple files at the same time, side by side (+ it is the Python pep std)

## Names
Take the time to choose descriptive names. Naming things is a great power, it comes with great responsabilities [CC-N1]

- Some good characteristics : intention-revealing, pronounceable, searchable. [CC-Chapt1]
- Don't use Hungarian notation or member prefixes [CC-Chapt1]
- Use noun/noun phrase naming for types, verb/verb phrases for methods, not only adjectives. Avoid words like Manager, Processor, Data or Info. [CC-Chapt1]
- Don't pick names that communicate implementationi [CC-N2]
- Use standard nomenclatures where possible [CC-N3]
- Unambigous names [CC-N4]
- Use long names for long scopes : 'i' is ok for small loops [CC-N5]
- Names should describe side-effects [CC-N7]
- Function names should say what they do : you can tell it from a call, without looking at the definition [CC-G20] Common smells:
    * Obvious behaviour is unimplemented [CC-G2]
    * Incorrect behaviour at the boundaries [CC-G3]

## Functions smells
- Too long [CC-Chapt2]
- Do too many things : split long imperative code in short functions that do ONE thing, and take good care of their naming [CC-Chapt2] [CC-G30]
- Has too many levels of abstraction [CC-Chapt2]
- Too many arguments : best are no-arg, one arg, two arg and possibly 3 args. Avoid 4+ [CC-F1]
- Output arguments [CC-F2]
- Flag or selector arguments (boolean) [CC-F3] [CC-G15]
- A () { B; C; D; } is better than A () { B } B () { C } C () { D } [Brandon Rhodes]

## Comments smells
- Inappropriate information : change history, author... [CC-C1]
- Obsolete comment [CC-C2]
- Redundant comment : e.g. useless Javadoc [CC-C3]
- Poorly written comment : don't ramble, don't state the obvious, be brief [CC-C4]
- Commented-out code [CC-C5]
Don't use comments when you can use a function/variable to expresse the intent [CC-Chapt4]

## Error handling
- Handle as many errors as possible locally, but export as few errors as possible [SDP]
- Use unchecked exceptions over return codes & checked exceptions
- Provide context with exceptions : chain them [CC-Chapt7]
- DO NOT RETURN/PASS NULL : C.A.R. Hoare "billion-dollar mistake". Alternatives:
    * NullObject & SpecialCase patterns
    * Empty collection
    * Raise an exception
    * Use a functional "Optional" construct

## Build system smells
- Build requires more than one step [CC-E1]
- Tests require more than one step [CC-E2]
- Build is too long to complete

## Tests
- F.I.R.S.T tests : Fast Independent Repeatable Self-Validating Timely (written just before prod code) [CC-Chapt9]
- One assert/concept per test [CC-Chapt9]
- Insufficient tests : use a coverage tool ! [CC-T1] [CC-T2] An ignored test is a question about an ambiguity [CC-T4]
- Take special care to test boundary conditions [CC-T5]
- Exhaustively test near bugs [CC-T6]
- Write learning tests [CC-Chapt8]
- Use manual try/catch and not @Test(expected) on big tests
- Don't overuse Mocks [DOM]
* Tests can be harder to understand
* Tests can be harder to maintain
* Tests can provide less assurance that your code is working properly
- Know Your Test Doubles [KYTD]
* A stub has no logic, and only returns what you tell it to return
* A mock has expectations about the way it should be called, and a test should fail if it’s not called that way. Mocks are used to test interactions between objects.
* A fake doesn’t use a mocking framework: it’s a lightweight implementation of an API that behaves like the real implementation, but isn't suitable for production.

### Why unit tests ? [PP-Chapt34]
- build trust in your code
- build regression tests, helpful for later refactoring
- show examples of how to use your code
- explicitely details the code behaviour on corner cases

## Code review > TDD [CRoTDD]
* TDD: automated, easy to follow, autonomously done
* CR: increase code quality & reduce defect rate, mutual learning, feeling better (get team mates attention + share responsability -> team building)
* Do it well: use tools; make it part of the process; detail purpose & testing; track CR ids in commits; no meeting -> can be done at anytime; make it constructive, informal & fun

## General
- Favor immutable data structures. Use the builder pattern for constructors with many parameters : MyClass.newMyClass("initial_param").withParamA("A").withParamB("B").build()
- Favor idempotent operations, i.e. "that has no additional effect if it is called more than once with the same input parameters".

- Data/Object anti-symetry : both have different use-cases [CC-Chapt6]
    * "Objects hide their data behind abstractions and expose functions that operate one data"
    * "Data structures expose their data and have no meaningful functions"
- for high performances, OOP is a bad idea, think Data Oriented Design instead

- Avoid multiple languages in one source file [CC-G1]
- Use the idioms of the programming language employed, aka "Don't write C code in Java"
- When debugging, **THINK** before going on step-by-step debug mode [RobPikeKenThompson]

## Fun facts
- OCTDD : Obsessive Compulsive Test Driven Development
- Doug McIlroy replacement for Donald Knuth's 10+ pages of Pascal illustrating literate programming: 6 lines of shell
tr -cs A-Za-z '\n' |
tr A-Z a-z |
sort |
uniq -c |
sort -rn |
sed ${1}q
