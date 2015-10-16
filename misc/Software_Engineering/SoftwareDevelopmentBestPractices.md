Software Development Best Practices
===================================

## References
- [CC-\\w\\d+] : Clean Code - Robert C. Martin - Ed. Prentice Hall
- [PP] : The Pragmatic Programmer - Andrew Hunt & David Thomas - Ed. Addison-Wesley : http://blog.codinghorror.com/a-pragmatic-quick-reference/
- [AOSA] : [The Architecture of Open Source Applications](http://www.aosabook.org) - Amy Brown & Greg Wilson
- [JP] : Java Puzzlers - Joshua Bloch & Neal Gafter - Ed. Addison-Wesley
- [SDP] : [Software Design Philosophy - John Ousterhout](//ramcloud.stanford.edu/wiki/display/ramcloud/Software+Design+Philosophy)
- [97TEPSK] : [97 Things Every Programmer Should Know](http://programmer.97things.oreilly.com/wiki/index.php/Contributions_Appearing_in_the_Book)
- [DOM] : [Don't overuse mocks](http://googletesting.blogspot.com/2013/05/testing-on-toilet-dont-overuse-mocks.html)
- [KYTD] : [Know your test doubles](http://googletesting.blogspot.com/2013/07/testing-on-toilet-know-your-test-doubles.html)
- [CRoTDD] : [CR over TDD](http://svenpet.com/2014/01/07/better-code-reviews/)
- [JC-PI] : [John Carmack on Parallel Implementations](http://www.altdev.co/2011/11/22/parallel-implementations/)
- [RobPikeKenThompson] : [What Rob Pike learned from KenThompson](http://www.informit.com/articles/article.aspx?p=1941206)
- [The Problems With Acceptance Testing](http://www.jamesshore.com/Blog/The-Problems-With-Acceptance-Testing.html)
- [Cyclomatic] : [Quantifying the effect of TDD](http://www.keithbraithwaite.demon.co.uk/professional/presentations/2008/qcon/MeasureForMeasure.pdf) & [Cyclomatic complexity measure](http://www.keithbraithwaite.demon.co.uk/professional/software)
- [CRTP] : [Code review - Tools an process](http://www.slideshare.net/rantav/code-review) slides
- [BuildingADecentAPI](//philsturgeon.uk/blog/2013/07/building-a-decent-api/)
- [DistributedSystemsAndTheEndOfTheAPI](http://writings.quilt.org/2014/05/12/distributed-systems-and-the-end-of-the-api/)
- [AwkwardMicroservicesQuestions](http://blog.oshineye.com/2015/01/awkward-microservices-questions.html)
- [Functional Programming Patterns](http://www.slideshare.net/ScottWlaschin/fp-patterns-buildstufflt)
- [MicroservicesIncreaseOuterArchitectureComplexity](http://blogs.gartner.com/gary-olliffe/2015/01/30/microservices-guts-on-the-outside/)
- [How API schemas help you make web sites fast](http://gilesbowkett.blogspot.be/2015/01/why-panda-strike-wrote-fastest-json.html#apis-and-json-schema)
- [How to design a rest API](http://blog.octo.com/en/design-a-rest-api/) : includes discussion on URIs, query strings, content negotiation, CORS, Jsonp, HATEOAS and HTTP errors
- [RESTful API design refcard](http://blog.octo.com/wp-content/uploads/2014/10/RESTful-API-design-OCTO-Quick-Reference-Card-2.2.pdf)
- [Comparing the Defect Reduction Benefits of Code Inspection and Test-Driven Development](http://neverworkintheory.org/2011/08/31/comparing-the-defect-reduction-benefits-of-code-inspection-and-test-driven-development.html)
- [TestPyramid](http://martinfowler.com/bliki/TestPyramid.html) & [IceCreamConeAntipattern](http://watirmelon.com/2012/01/31/introducing-the-software-testing-ice-cream-cone/)
- [John Carmack discusses the art and science of software engineering](//blogs.uw.edu/ajko/2012/08/22/john-carmack-discusses-the-art-and-science-of-software-engineering/): "It’s about social interactions between the programmers or even between yourself spread over time" + "we talk about functional programming and lambda calculus and monads and this sounds all nice and sciency, but it really doesn’t affect what you do in software engineer­ing there, these are all best practices, and these are things that have shown to be helpful in the past, but really are only helpful when people are making certain classes of mistakes" + daily code reviews + the code you write may well exist a decade from now
- [The microservices cargo cult](http://www.stavros.io/posts/microservices-cargo-cult/)

My rule #1 : Follow standard conventions within a team [CC-G24]

## Main "mantras"
- Boy Scout Rule & Broken Window Theory
- KISS & YAGNI : Keep It Simple, Stupid & You Aren't Gonna Need It
- Duplication : DRY ! Once, and only once. [CC-G5]
    switch/case OR if/else chain -> polymorphism if appears more than once [CC-G23]
    similar algorithm            -> template method / strategy pattern
- Code Fearlessly & implement alternative code versions in parallel [JC-PP]
- "About 97% of the time: **premature optimization is the root of all evil**." - Donald Knuth, 1974
- "Optimization work is so appealing, with incremental and objective rewards, but it is easy to overestimate value relative to other tasks" - John Carmack, 2015
- Rob Pike's 5 rules of optimizations:
    - Rule 1. You can't tell where a program is going to spend its time. Bottlenecks occur in surprising places, so don't try to second guess and put in a speed hack until you've proven that's where the bottleneck is.
    - Rule 2. Measure. Don't tune for speed until you've measured, and even then don't unless one part of the code overwhelms the rest.
    - Rule 3. Fancy algorithms are slow when n is small, and n is usually small. Fancy algorithms have big constants. Until you know that n is frequently going to be big, don't get fancy. (Even if n does get big, use Rule 2 first.)
    - Rule 4. Fancy algorithms are buggier than simple ones, and they're much harder to implement. Use simple algorithms as well as simple data structures.
    - Rule 5. Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident. Data structures, not algorithms, are central to programming.
- "Programs must be written for people to read, and only incidentally for machines to execute." - Hal Abelson
- " Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live. Code for readability." - John Woods
- write greppable code
- fail fast
- Tony Hoare null "billion-dollar mistake"

## Design principles
where "Design" = Architecture / Organisation of the software logic

SE = software entity : class, module, function...

SOLID:
- Single Responsability Principle : every SE should have a single responsibility, and that responsibility should be entirely encapsulated by the SE
    Aka Common Closure Principle : any change to the software should only have a very local impact
- Open/Closed Principle : SE should be open for extension, but closed for modification
- Liskov substitution principle: objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program.
- Interface segregation principle: many client-specific interfaces are better than one general-purpose interface
- Dependency inversion principle: one should depend upon Abstractions, do not depend upon concretions.

Law of Demeter : each SE should have only limited knowledge about other SEs. Write "shy code". Talk to friends; Don’t talk to strangers [CC-G36]

DTO/DAO:
- Data Transfer Object : used to transfer the data between classes and modules of your application. DTO should only contain private fields for your data, getters, setters and constructors. It is not recommended to add business logic methods to such classes, but it is OK to add some util methods.
- Data Access Object encapsulate the logic for retrieving, saving and updating data in your data storage (a database, a file-system, whatever).

On APIs : [BuildingADecentAPI], [DistributedSystemsAndTheEndOfTheAPI], ![xkcd/1481](http://imgs.xkcd.com/comics/api.png), [How to design a rest API], [RESTful API design refcard]
+ use a JSON Schema for validation ! : [How API schemas help you make web sites fast]
+ similarly: IDL, Interface Description Language. E.g. ApacheThrift, Protocol Buffers, SWIG...
+ WSDL = Web Service Description Language (in xml, often used with SOAP)
+ representation for RESTful APIs: Swagger / RAML / API Blueprint / APIDOC

On microservices : [AwkwardMicroservicesQuestions], [MicroservicesIncreaseOuterArchitectureComplexity], [The microservices cargo cult] : they add moving parts and interdependencies, perf overhand and data segregation, and in the end more complexity

## Design smells
- "Thin" classes. Ideally, a class should have a very simple interface that hides a lot of functionality and internal complexity. [SDP]
    Too much information : hide you data, hide your utility functions, hide your constants & temporaries, concentrate on keeping small interfaces to keep coupling low [CC-G8]
- Code at wrong level of abstraction : e.g. functions should descend only one level of abstraction [CC-G6] [CC-G34]
- Classes designed around algorithms or time order (i.e. collect all the things that happen at one point in time into a single class) : design classes around INFORMATION [SDP]
- "It is almost always incorrect to begin the decomposition of a system into modules on the basis of a flowchart. We propose instead that one begins with a list of difficult design decisions or design decisions which are likely to change." - [On the criteria to be used in decomposing systems into modules](http://web.archive.org/web/20121017182047/http://sunnyday.mit.edu/16.355/parnas-criteria.html), D. Parnas -> introduces the idea that we should use modularity to hide design decisions - things which could change.
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
- Don't overuse Mocks [DOM] or they'll become **mockeries**
* Tests can be harder to understand
* Tests can be harder to maintain
* Tests can provide less assurance that your code is working properly
- Know Your Test Doubles [KYTD]
* A stub has no logic, and only returns what you tell it to return
* A mock has expectations about the way it should be called, and a test should fail if it’s not called that way. Mocks are used to test interactions between objects.
* A fake doesn’t use a mocking framework: it’s a lightweight implementation of an API that behaves like the real implementation, but isn't suitable for production.
* test your code opening files with /dev/full that always returns error code ENOSPC (meaning “No space left on device”)
* GUI testing, e.g. with Selenium: Capybara, SauceLabs, RobotFramework
* the [TestPyramid]: ![](http://martinfowler.com/bliki/images/testPyramid/pyramid.png) : more low-level tests than high level end-to-end tests

### Why unit tests ? [PP-Chapt34]
- build trust in your code
- build regression tests, helpful for later refactoring
- show examples of how to use your code
- explicitely details the code behaviour on corner cases

## Code review > TDD [CRoTDD]
cf. [Comparing the Defect Reduction Benefits of Code Inspection and Test-Driven Development]
* You **need** TDD !! (or at least some kind of automated systematic testing) [QETDDM]
* TDD: automated, easy to follow, autonomously done
* CR: increase code quality & reduce defect rate, mutual learning, feeling better (get team mates attention + share responsability -> team building) - For a introductory presentation: [CRTP]
* Do it well: use proper tools, including automated static analysis (findbugs, ArtisticStyle for C/C++/Java, checkstyle + [Cyclomatic]), syntax-checkers...); make it part of the process; detail purpose & testing; track CR ids in commits; no meeting -> can be done at anytime; make it constructive, informal & fun

## Functional programming
cf. [Functional Programming Patterns]
- _"Don't trust the name - trust the signature"_
- "Domain modelling pattern" : use types to represent constraints, _avoid "primitive obsession"_
- Tail Call Optimization (TCO) : sometimes implemented with a _trampoline_ design pattern

## General
- Favor immutable data structures. Use the builder pattern for constructors with many parameters : MyClass.newMyClass("initial_param").withParamA("A").withParamB("B").build()
- Favor idempotent operations, i.e. "that has no additional effect if it is called more than once with the same input parameters".

- Data/Object anti-symetry : both have different use-cases [CC-Chapt6]
    * "Objects hide their data behind abstractions and expose functions that operate one data"
    * "Data structures expose their data and have no meaningful functions"
- for high performances, OOP is a bad idea, think Data Oriented Design instead

- Avoid multiple languages in one source file [CC-G1]
- Use the idioms of the programming language employed, aka "Don't write C code in Java"
- When debugging, **THINK** before going on step-by-step debug mode [RobPikeKenThompson]. [A longer quote on ptrint-traces debugging VS debuggers](http://taint.org/2007/01/08/155838a.html)

## The UNIX Philosophy by Mike Gancarz
1. Small is beautiful.
2. Make each program do one thing well.
3. Build a prototype as soon as possible.
4. Choose portability over efficiency.
5. Store data in flat text files.
6. Use software leverage to your advantage.
7. Use shell scripts to increase leverage and portability.
8. Avoid captive user interfaces.
9. Make every program a filter.

## [On beeing a senior engineer](http://www.kitchensoap.com/2012/10/25/on-being-a-senior-engineer/)
- Mature engineers seek out constructive criticism of their designs.
- Mature engineers understand the non-technical areas of how they are perceived.
- Mature engineers do not shy away from making estimates, and are always trying to get better at it.
- Mature engineers have an innate sense of anticipation, even if they don’t know they do.
- Mature engineers understand that not all of their projects are filled with rockstar-on-stage work.
- Mature engineers lift the skills and expertise of those around them.
- Mature engineers make their trade-offs explicit when making judgements and decisions.
- Mature engineers don’t practice CYAE (“Cover Your Ass Engineering”)
- Mature engineers are empathetic.
- Mature engineers don’t make empty complaints.
- Mature engineers are aware of cognitive biases
    * [Self-Serving Bias](//en.wikipedia.org/wiki/Self-serving_bias)
    * [Fundamental Attribution Error](//en.wikipedia.org/wiki/Fundamental_attribution_error)
    * [Hindsight Bias ](//en.wikipedia.org/wiki/Hindsight_bias)
    * [Outcome Bias](//en.wikipedia.org/wiki/Outcome_bias)
    * [Planning Fallacy](//en.wikipedia.org/wiki/Planning_fallacy)
    * [Belief bias](//en.wikipedia.org/wiki/Belief_bias)
    * [Confirmation bias](//en.wikipedia.org/wiki/Confirmation_bias) & [Experimenter's bias](//en.wikipedia.org/wiki/Experimenter%27s_bias)
    * [Sunk cost fallacy](//en.wikipedia.org/wiki/Sunk_costs#Loss_aversion_and_the_sunk_cost_fallacy)
    * [Cargo cult](//en.wikipedia.org/wiki/Cargo_cult) of a new technology / design pattern
    * [Groupthink symptoms](//en.wikipedia.org/wiki/Groupthink#Symptoms)
+ [The Role of a Senior Developper](http://mattbriggs.net/blog/2015/06/01/the-role-of-a-senior-developer/)

### The Ten Commandments of Egoless Programming
- Understand and accept that you will make mistakes.
- You are not your code.
- No matter how much “karate” you know, someone else will always know more.
- Don’t rewrite code without consultation.
- Treat people who know less than you with respect, deference, and patience.
- The only constant in the world is change. Be open to it and accept it with a smile.
- The only true authority stems from knowledge, not from position.
- Fight for what you believe, but gracefully accept defeat.
- Don’t be “the coder in the corner.”
- Critique code instead of people – be kind to the coder, not to the code.

## Fun quotes
- OCTDD : Obsessive Compulsive Test Driven Development
- Doug McIlroy replacement for Donald Knuth's 10+ pages of Pascal illustrating literate programming: 6 lines of shell
    tr -cs A-Za-z '\n' |
    tr A-Z a-z |
    sort |
    uniq -c |
    sort -rn |
    sed ${1}q
- "The bearing of a child takes nine months, no matter how many women are assigned. Adding manpower to a late software project makes it later." Fred Brooks - "The Mythical Man-Month"
- "Hofstadter's Law: It always takes longer than you expect, even when you take into account Hofstadter's Law" - GEB
- "Programmers always confuse Halloween with Christmas because Oct 31 == Dec 25"
- "La Cathédrale et le Bazar" - Essai on Open Source & Proprietary Software
- "If you can not measure it, you can not improve it." Lord Kelvin
- the phrase software "patch" is from a physical patch applied to Mark 1 paper tape to modify the program: https://chezsoi.org/lucas/ThePatch.jpg
- "Object-oriented programming is an exceptionally bad idea which could only have originated in California" - E.W. Dijkstra
"You probably know that arrogance, in computer science, is measured in nanodijkstras" - Alan Kay
- "Expertise is not about picking good solution, it is about picking the future bad one at the right time." Eric Bréhault, Makina Corpus
- "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations" - Mel Conway, 1968
- [The Parable of the Two Programmers](http://www.csd.uwo.ca/~magi/personal/humour/Computer_Audience/The%20Parable%20of%20the%20Two%20Programmers.html)
- [The story of Mel](http://www.catb.org/jargon/html/story-of-mel.html) :
"I have often felt that programming is an art form,
whose real value can only be appreciated
by another versed in the same arcane art;
there are lovely gems and brilliant coups
hidden from human view and admiration, sometimes forever,
by the very nature of the process.
You can learn a lot about an individual
just by reading through his code,
even in hexadecimal."
