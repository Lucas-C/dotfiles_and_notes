Software Development Best Practices
===================================

::: toc
[[toc]]
:::

## References
- [CC-\\w\\d+](http://fr.slideshare.net/hebel/clean-code-vortrag032009pdf) : Clean Code - Robert C. Martin - Ed. Prentice Hall
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
- [CRTP] : [Code review - Tools and process](http://www.slideshare.net/rantav/code-review) slides
- [BuildingADecentAPI](//philsturgeon.uk/blog/2013/07/building-a-decent-api/)
- [DistributedSystemsAndTheEndOfTheAPI](http://writings.quilt.org/2014/05/12/distributed-systems-and-the-end-of-the-api/)
- [AwkwardMicroservicesQuestions](http://blog.oshineye.com/2015/01/awkward-microservices-questions.html)
- [Functional Programming Patterns](http://www.slideshare.net/ScottWlaschin/fp-patterns-buildstufflt)
- [MicroservicesIncreaseOuterArchitectureComplexity](http://blogs.gartner.com/gary-olliffe/2015/01/30/microservices-guts-on-the-outside/)
- [How API schemas help you make web sites fast](http://gilesbowkett.blogspot.be/2015/01/why-panda-strike-wrote-fastest-json.html#apis-and-json-schema)
- [How to design a REST API](http://blog.octo.com/en/design-a-rest-api/) : includes discussion on URIs, query strings, content negotiation, CORS, Jsonp, HATEOAS and HTTP errors
- [RESTful API design refcard](http://blog.octo.com/wp-content/uploads/2014/10/RESTful-API-design-OCTO-Quick-Reference-Card-2.2.pdf)
- [Comparing the Defect Reduction Benefits of Code Inspection and Test-Driven Development](http://neverworkintheory.org/2011/08/31/comparing-the-defect-reduction-benefits-of-code-inspection-and-test-driven-development.html)
- [TestPyramid](http://martinfowler.com/bliki/TestPyramid.html) & [IceCreamConeAntipattern](http://watirmelon.com/2012/01/31/introducing-the-software-testing-ice-cream-cone/)
- [John Carmack discusses the art and science of software engineering](//blogs.uw.edu/ajko/2012/08/22/john-carmack-discusses-the-art-and-science-of-software-engineering/): "It’s about social interactions between the programmers or even between yourself spread over time" + "we talk about functional programming and lambda calculus and monads and this sounds all nice and sciency, but it really doesn’t affect what you do in software engineer­ing there, these are all best practices, and these are things that have shown to be helpful in the past, but really are only helpful when people are making certain classes of mistakes" + daily code reviews + the code you write may well exist a decade from now
- [The microservices cargo cult](http://www.stavros.io/posts/microservices-cargo-cult/)
- [LatencyNumbersEveryProgrammerShouldKnow](https://gist.github.com/hellerbarde/2843375)
- [ResponseTimes-The3ImportantLimits](http://www.nngroup.com/articles/response-times-3-important-limits/)
- [What happens when the Board Of Directors begins to panic?](http://www.smashcompany.com/business/what-happens-when-the-board-of-directors-begins-to-panic)
- [Why code review beats testing: evidence from decades of programming research](https://kev.inburke.com/kevin/the-best-ways-to-find-bugs-in-your-code/)
- [Best practices for code review](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)
- [Why Should Software Architects Write Code](http://blog.ieeesoftware.org/2016/02/why-should-software-architects-write.html)
- [A Guide to Naming Variables](http://a-nickels-worth.blogspot.fr/2016/04/a-guide-to-naming-variables.html)
- [Why do record/replay tests of web applications break?](https://blog.acolyer.org/2016/05/30/why-do-recordreplay-tests-of-web-applications-break)
- [MicroservicesPleaseDont](https://blog.komand.com/microservices-please-dont)
- [LogstashAlternatives][https://sematext.com/blog/2016/09/13/logstash-alternatives/] : Filebeat, Fluentd, rsyslog, syslog-ng & Logagent
- [ModernSoftwareOverEngineeringMistakes](https://medium.com/@rdsubhas/10-modern-software-engineering-mistakes-bc67fbef4fc8#.3y051ocdz)
- [WhyYouShouldUseAMonorepo](http://www.drmaciver.com/2016/10/why-you-should-use-a-single-repository-for-all-your-companys-projects/)
- [WhenToRepeatYourself](http://devblog.songkick.com/2016/08/31/when-to-repeat-yourself/)
- [InternetScaleServicesChecklist](https://gist.github.com/acolyer/95ef23802803cb8b4eb5)
- [WhatsWrongWithGit?AConceptualDesignAnalysis](https://blog.acolyer.org/2016/10/24/whats-wrong-with-git-a-conceptual-design-analysis/)
- [Simple Standard Service Endpoints](https://github.com/beamly/SE4/blob/master/SE4.md)
- [DesignPatternForHumans](https://github.com/kamranahmedse/design-patterns-for-humans)
- [SystemDesignPrimer](https://github.com/donnemartin/system-design-primer)
- [CommandQueryResponsibilitySegregation](http://blog.eleven-labs.com/en/cqrs-pattern-2/)
- [LavaLayerAntiPattern](http://mikehadlow.blogspot.fr/2014/12/the-lava-layer-anti-pattern.html)
- [DontReadYourLogs](https://medium.com/@chimeracoder/dont-read-your-logs-13586c790202)
- [PreMergeCodeReviews](http://verraes.net/2013/10/pre-merge-code-reviews/)
- [Architecture Review Working Group : Multiple Perspectives On Technical Problems and Solutions](https://www.kitchensoap.com/2017/08/12/multiple-perspectives-on-technical-problems-and-solutions/)
- [How to Do Code Reviews Like a Human](https://mtlynch.io/human-code-reviews-1/)
- [Testing Microservices, the sane way](https://medium.com/@copyconstruct/testing-microservices-the-sane-way-9bb31d158c16)
- [Understanding RPC Vs REST For HTTP APIs](https://www.smashingmagazine.com/2016/09/understanding-rest-and-rpc-for-http-apis/)
- [PUT vs PATCH vs JSON-PATCH](https://blog.apisyouwonthate.com/put-vs-patch-vs-json-patch-208b3bfda7ac)
- [Regular Expressions: Now You Have Two Problems](https://blog.codinghorror.com/regular-expressions-now-you-have-two-problems/)
- [Joel On Software - Things You Should Never Do](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/)
- [Why "Agile" and especially Scrum are terrible](https://michaelochurch.wordpress.com/2015/06/06/why-agile-and-especially-scrum-are-terrible/)

My rule #1 : Follow standard conventions within a team [CC-G24]

## Main design "mantras"
- KISS & YAGNI : Keep It Super Simple & You Aren't Gonna Need It
- Duplication : DRY ! Once, and only once. [CC-G5] but not too DRY: [WhenToRepeatYourself]
    * switch/case OR if/else chain -> polymorphism if appears more than once [CC-G23]
    * similar algorithm            -> template method / strategy pattern
- less is more : "best code is no code at all" & "complexity is our worst enemy"
- fail fast
- [Regular Expressions: Now You Have Two Problems](https://blog.codinghorror.com/regular-expressions-now-you-have-two-problems/)
- Favor immutable data structures. Use the builder pattern for constructors with many parameters : MyClass.newMyClass("initial_param").withParamA("A").withParamB("B").build()
- Favor idempotent operations, i.e. "that has no additional effect if it is called more than once with the same input parameters".
- Smalltalk first principle: "If a system is to serve the creative spirit, it must be entirely comprehensible to a single individual"

> 13. Perfection (in design) is achieved not when there is nothing more to add, but rather when there is nothing more to take away.
FROM: The Cathedral and the Bazaar by Eric S. Raymond (Attributed to Antoine de Saint-Exupéry)

> They did it by making the single worst strategic mistake that any software company can make:
> They decided to rewrite the code from scratch.

> There’s a subtle reason that programmers always want to throw away the code and start over.
> The reason is that they think the old code is a mess.
> And here is the interesting observation: they are probably wrong.
FROM: [Joel On Software - Things You Should Never Do]

### On optimization & readability
- "About 97% of the time: **premature optimization is the root of all evil**." - Donald Knuth, 1974
- "Optimization work is so appealing, with incremental and objective rewards, but it is easy to overestimate value relative to other tasks" - John Carmack, 2015
- Rob Pike's 5 rules of optimizations:
    - Rule 1. You can't tell where a program is going to spend its time. Bottlenecks occur in surprising places, so don't try to second guess and put in a speed hack until you've proven that's where the bottleneck is.
    - Rule 2. Measure. Don't tune for speed until you've measured, and even then don't unless one part of the code overwhelms the rest.
    - Rule 3. Fancy algorithms are slow when n is small, and n is usually small. Fancy algorithms have big constants. Until you know that n is frequently going to be big, don't get fancy. (Even if n does get big, use Rule 2 first.)
    - Rule 4. Fancy algorithms are buggier than simple ones, and they're much harder to implement. Use simple algorithms as well as simple data structures.
    - Rule 5. Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident. Data structures, not algorithms, are central to programming.

- "Programs must be written for people to read, and only incidentally for machines to execute." - Hal Abelson
- "Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live. Code for readability." - John Woods
- write greppable code

### Performance-oriented design advices
- Data/Object anti-symetry : both have different use-cases [CC-Chapt6]
    * "Objects hide their data behind abstractions and expose functions that operate one data"
    * "Data structures expose their data and have no meaningful functions"
- for high performances, OOP is a bad idea, think Data Oriented Design instead

- know the order of magnitude it takes to perform various operations on a computer : cf. [LatencyNumbersEveryProgrammerShouldKnow] & [ResponseTimes-The3ImportantLimits] :
    * 0.1 second is about the limit for having the user feel that the system is reacting instantaneously, meaning that no special feedback is necessary except to display the result.
    * 1.0 second is about the limit for the user's flow of thought to stay uninterrupted, even though the user will notice the delay.
    Normally, no special feedback is necessary during delays of more than 0.1 but less than 1.0 second, but the user does lose the feeling of operating directly on the data.
    * 10 seconds is about the limit for keeping the user's attention focused on the dialogue.
    For longer delays, users will want to perform other tasks while waiting for the computer to finish, so they should be given feedback indicating when the computer expects to be done.
    Feedback during the delay is especially important if the response time is likely to be highly variable, since users will then not know what to expect.


## Good work habits / self-organization
![](https://chezsoi.org/lucas/wwcb/photos/BoyScoutRule.jpg)
- [Boy Scout Rule](http://programmer.97things.oreilly.com/wiki/index.php/The_Boy_Scout_Rule) & Broken Window Theory
- Code Fearlessly & implement alternative code versions in parallel [JC-PP]
- When debugging, **THINK** before going on step-by-step debug mode [RobPikeKenThompson]. [A longer quote on print-traces debugging VS debuggers](http://taint.org/2007/01/08/155838a.html)
- [Rubber duck programming](https://en.wikipedia.org/wiki/Rubber_duck_debugging)

### Be rigorous and clean after yourself
- Be consistent : be careful with the conventions you choose, and follow them strictly. E.g. stick with one word per concept. [CC-G11]
- Structure over convention : e.g. base clase enforce interface whereas switch/case can contain anything [CC-G27]
- Don't override safeties : e.g. turning off compiler warnings or some failing tests. Think about Chernobyl ! [CC-G4]
- Remove dead code : unused function, impossible "if" condition, useless try/catch... [CC-F4] [CC-G9] [CC-G12]

### [On beeing a senior engineer](http://www.kitchensoap.com/2012/10/25/on-being-a-senior-engineer/)
- Mature engineers seek out constructive criticism of their designs.
- Mature engineers understand the non-technical areas of how they are perceived.
- Mature engineers do not shy away from making estimates, and are always trying to get better at it.
(another take on that subject from [Why "Agile" and especially Scrum are terrible]:
The worst thing about estimates is that they push a company in the direction of doing work that’s estimable.
Anything that’s actually worth doing has a non-zero chance of failure and too many unknown unknowns for estimates to be useful.)
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
    * [Sunk cost fallacy](//en.wikipedia.org/wiki/Sunk_costs#Loss_aversion_and_the_sunk_cost_fallacy) : misgivings about "wasting" resources, feeling you have to do something because you've passed the point of no return aka "coûts irrécupérables" aka "effet Concorde" aka "Vietnam effect" cf. [Crétin de Cerveau](https://www.youtube.com/watch?v=GCmfXMMhRzk)
    * [Cargo cult](//en.wikipedia.org/wiki/Cargo_cult) of a new technology / design pattern
    * [Groupthink symptoms](//en.wikipedia.org/wiki/Groupthink#Symptoms)
    * Spurious correlations: Correlation != causality, aka "post hoc ergo propter hoc" aka "effet cigogne" (cf. eponymous website & e-penser video "le lieu le plus dangereux de France" = le lit)
    * [Dunning-Kruger Effect](//en.wikipedia.org/wiki/Dunning%E2%80%93Kruger_effect) : "relatively unskilled individuals suffer from illusory superiority, mistakenly assessing their ability to be much higher than it really is"
    * [Simpson’s Paradox](//blog.forrestthewoods.com/my-favorite-paradox-14fab39524da)
    * [Imposter Syndrom](https://www.laserfiche.com/simplicity/shut-up-imposter-syndrome-i-can-too-program/) + https://opensource.com/sitewide-search?search_api_views_fulltext=imposter%20syndrome
    * [Completion Bias](http://jkglei.com/momentum/)
    * [XY Problem](http://xyproblem.info)
    * [anchoring effect](https://en.wikipedia.org/wiki/Anchoring) : when people consider a particular value for an unknown quantity before estimating that quantity
    * [the halo effect](https://en.wikipedia.org/wiki/Halo_effect) : the tendency to like (or dislike) everything about a person—including things you have not observed

[The Role of a Senior Developper](http://mattbriggs.net/blog/2015/06/01/the-role-of-a-senior-developer/):
- A senior developer [...] is obsessed with simplicity.
- senior developer [...] understand that there is no “Right Way” to build software
- A senior developer understands that everything in our field involves tradeoff
- A senior developer thinks of more than just themselves.
- A senior developer will understand that this job is to provide solutions to problems, not write code
- A senior developer understands that you cannot do everything yourself, and that their primary role is to help their team get better
- A senior developer understands that leadership is not about power, it is about empowerment. It is not about direction, it is about serving.

"When facing extremely short, ambitious deadlines, one knows there are a dozen good things one can do, but very little feels justifiable in the face of a crisis, except writing code as fast as possible." [What happens when the Board Of Directors begins to panic?]

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

CQRS pattern = [CommandQueryResponsibilitySegregation] : split the code & logic between the Query path (DB -> UI) & Command path (UI -> DB)

POLA = Principle of least astonishment (or surprise => POLS) : "People are part of the system. The design should match the user's experience, expectations, and mental models.
    If a necessary feature has a high astonishment factor, it may be necessary to redesign the feature."

[DesignPatternForHumans] : Ultra-simplified explanation to design patterns

[SystemDesignPrimer]: how to design large-scale systems, with diagram-based examples -> Performance vs scalability / Latency vs throughput / Availability vs consistency / DNS & CDN / Load balancer / Reverse proxy / Microservices / Service discovery / RDBMS & NoSQL / Cache / Asynchronism / Communication / Security
cf. also [DistributedSystemsAndTheEndOfTheAPI]

[Architecture Review Working Group : Multiple Perspectives On Technical Problems and Solutions]:
> Excellent, it sounds like you have a hypothesis! We are gonna do an architecture review.
> If it’s as obvious a solution as you think it is, it should be easy for the rest of the org to come to the same conclusion, and that will make implementing and maintaining it that much easier.
> If it has some downsides that aren’t apparent, we will at least have a chance to tease those out!

### Resilience patterns
FROM: https://docs.microsoft.com/en-us/azure/architecture/patterns/
- Timeouts
- Retry : handle anticipated, temporary failures of a partner service or network resource by transparently retrying an operation that failed, ideally with an exponential backoff logic
- Back Pressure (ex: `Retry-After` HTTP header)
- Circuit Breaker : preserve a remote service or resource that may fall down
- Health Endpoint Monitoring : Implement functional checks in an application that external tools can access through exposed endpoints at regular intervals.
- Asynchronous Communication
- Fail Fast
- Idempotency
- Stateless
- Bulkhead : isolate elements of an application into pools so that if one fails, the others will continue to function.
Named because it resembles the sectioned partitions of a ship's hull: if it is compromised, only the damaged section fills with water, which prevents the ship from sinking.
- Compensating Transaction : Undo the work performed by a series of steps, which together define an eventually consistent operation.
- Extensive Parameter Checking: often neglected
> Be conservative in what you send, be liberal in what you accept (Postel's law / Robustness principle)

### APIs, REST vs RPC, microservices

![xkcd/1481](http://imgs.xkcd.com/comics/api.png)

cf. [BuildingADecentAPI]

On microservices : [AwkwardMicroservicesQuestions], [MicroservicesIncreaseOuterArchitectureComplexity], [The microservices cargo cult], [MicroservicesPleaseDont] : they add moving parts and interdependencies, perf overhand and data segregation, and in the end more complexity

REST = Representational State Transfer: [How to design a REST API], [RESTful API design refcard]
cf. also OData ISO/IEC approved, OASIS standard, defining a set of best practices for building and consuming RESTful APIs
or the [{json:api}](http://jsonapi.org) spec, which has a [very detailed description of how to return errors](http://jsonapi.org/format/#errors)

![](http://martinfowler.com/articles/images/richardsonMaturityModel/overview.png)

(taken from http://spring.io/guides/tutorials/bookmarks/)
Dr. Leonard Richardson put together a maturity model that interprets various levels of compliance with RESTful principles, and grades them. It describes 4 levels, starting at level 0. Martin Fowler has a very good write-up on the maturity model

- Level 0: the Swamp of POX - at this level, we’re just using HTTP as a transport. You could call SOAP a Level 0 technology. It uses HTTP, but as a transport. It’s worth mentioning that you could also use SOAP on top of something like JMS with no HTTP at all. SOAP, thus, is not RESTful. It’s only just HTTP-aware.
- Level 1: Resources - at this level, a service might use HTTP URIs to distinguish between nouns, or entities, in the system. For example, you might route requests to /customers, /users, etc. XML-RPC is an example of a Level 1 technology: it uses HTTP, and it can use URIs to distinguish endpoints. Ultimately, though, XML-RPC is not RESTful: it’s using HTTP as a transport for something else (remote procedure calls).
- Level 2: HTTP Verbs - this is the level you want to be at. If you do everything wrong with Spring MVC, you’ll probably still end up here. At this level, services take advantage of native HTTP qualities like headers, status codes, distinct URIs, and more. This is where we’ll start our journey.
- Level 3: Hypermedia Controls - This final level is where we’ll strive to be. Hypermedia, as practiced using the HATEOAS ("HATEOAS" is a truly welcome acronym for the mouthful, "Hypermedia as the Engine of Application State") design pattern. Hypermedia promotes service longevity by decoupling the consumer of a service from intimate knowledge of that service’s surface area and topology. It describes REST services. The service can answer questions about what to call, and when. We’ll look at this in depth later.

[PUT vs PATCH vs JSON-PATCH] tl;dr :
> The existing HTTP PUT method only allows a complete replacement of a document. This proposal adds a new HTTP method, PATCH, to modify an existing HTTP resource.
cf. also the [JSON PATCH spec](http://jsonpatch.com)

[Partial resources](https://developers.google.com/youtube/v3/getting-started#partial) : `?part=A,B&fields=e,f`

+ use a JSON Schema for validation ! : [How API schemas help you make web sites fast]
+ similarly for protocols: IDL, Interface Description Language. E.g. ApacheThrift, Protocol Buffers, SWIG, DTD/XSD for XML...
+ WSDL = Web Service Description Language (in xml, often used with SOAP)
+ representation for RESTful APIs: Swagger==OpenAPI / API Blueprint / APIDOC
cf. https://apiary.io -> online APi editor with persistance on GitHub + auto-generated doc & server mocks + auto integration testing with [dredd](https://github.com/apiaryio/dredd) + has a free plan
+ follow simple standards for server status / healthcheck like [Simple Standard Service Endpoints]
+ alternative to REST: [JSON RPC](http://www.jsonrpc.org/specification) cf. [Understanding RPC Vs REST For HTTP APIs]!
  > REST brings some constraints, e.g. your API must be stateless (no session persistance)
  > RPC-based APIs are great for actions [while] REST-based APIs are great for modeling your domain

### The UNIX Philosophy by Mike Gancarz
1. Small is beautiful.
2. Make each program do one thing well.
3. Build a prototype as soon as possible.
4. Choose portability over efficiency.
5. Store data in flat text files.
6. Use software leverage to your advantage.
7. Use shell scripts to increase leverage and portability.
8. Avoid captive user interfaces.
9. Make every program a filter.

### Design smells
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
- [LavaLayerAntiPattern] :
> Try and have some sympathy and understanding for those who came before you.
> There was probably a good reason for why things were done the way they were. Be especially sympathetic to consistency,
> even if you don’t necessarily agree with the design or technology choices.


## Code programming best practices
- Use the idioms of the programming language employed, aka "Don't write C code in Java"
- Avoid multiple languages in one source file [CC-G1]

### Code intent should be obvious
- Understand the algorithm first [CC-G21]
- Don't be arbitrary, you must be able to justify any decision in your code [CC-G32]
- Use explanatory variables [CC-G19]
- Replace magic numbers with named constants + try to gather configuration [CC-G25]
- Conditionals : encapsulate them instead of making and/or combinations inline, avoid double negation [CC-G28] [CC-29]
- Obscured intent : in doubt, detail your motivation as comments [CC-G16]

### Code formatting
- Keep source files short !
- Write top-down code that reads like a narrative [CC-Chapt2]
- Vertical separation : define things close to where they are used [CC-G10]
- Do not line up variable names in a set of declarations/assignement statements [CC-Chapt5]
- keep lines length short (~80char) because it keeps the code readable + one can view multiple files at the same time, side by side (+ it is the Python pep std)

### Names
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
- [A Guide to Naming Variables] :
    * As coders our job is to communicate to human readers, not computers.
    * Names should communicate the coder's intent so the reader doesn't have to try to figure it out.
    * Boilerplate must be minimized, because it drains reviewers' ability to concentrate on the code.
    * Don't Put the Type in the Name
    * Use Teutonic Names Most of The Time
    * Move Simple Comments Into Variable Names: We prefer good names over comments but can't replace all comments.
    * Avoid Over-used Cliches: val, value, result, res, retval, tmp, temp, count, str
    * Use Idioms Where Meaning is Obvious
    * May Use Short Names Over Short Distances When Obvious -> I DISAGREE
    * Remove Thoughtless One-Time Variables -> I DISAGREE
    * Use Short OTVs to Break Up Long Lines & Complicated Expressions

### Functions smells
- Too long [CC-Chapt2]
- Do too many things : split long imperative code in short functions that do ONE thing, and take good care of their naming [CC-Chapt2] [CC-G30]
- Has too many levels of abstraction [CC-Chapt2]
- Too many arguments : best are no-arg, one arg, two arg and possibly 3 args. Avoid 4+ [CC-F1]
- Output arguments [CC-F2]
- Flag or selector arguments (boolean) [CC-F3] [CC-G15]
- A () { B; C; D; } is better than A () { B } B () { C } C () { D } [Brandon Rhodes]

### Comments smells
- Inappropriate information : change history, author... [CC-C1]
- Obsolete comment [CC-C2]
- Redundant comment : e.g. useless Javadoc [CC-C3]
- Poorly written comment : don't ramble, don't state the obvious, be brief [CC-C4]
- Commented-out code [CC-C5]
Don't use comments when you can use a function/variable to expresse the intent [CC-Chapt4]

### Error handling
- Handle as many errors as possible locally, but export as few errors as possible [SDP]
- Use unchecked exceptions over return codes & checked exceptions
- Provide context with exceptions : chain them [CC-Chapt7]
- DO NOT RETURN/PASS NULL : C.A.R. Hoare "billion-dollar mistake". Alternatives:
    * NullObject & SpecialCase patterns
    * Empty collection
    * Raise an exception
    * Use a functional "Optional" construct

### Logs
From [DontReadYourLogs]: "The next time you start to write a log line, ask yourself whether another observability tool would be a better fit."
What are logs used for ?
- metrics -> use `statsd.Histogram` or something similar
- error reporting -> use a dedicated tool like Sentry
- durable records -> use a DB
- debug tracing -> use something like Zipkin

### Build system smells
- Build requires more than one step [CC-E1]
- Tests require more than one step [CC-E2]
- Build is too long to complete

### Tests
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
    * [Why do record/replay tests of web applications break?] : "Our data suggests which categories of test breakages merit the greatest attention. Locators caused over 73% of the test breakages we observed, and attribute-based locators caused the majority of these."
    * the [TestPyramid]: ![](http://martinfowler.com/bliki/images/testPyramid/pyramid.png) : more low-level tests than high level end-to-end tests
- [Testing Microservices, the sane way]:
    * "Devs should be able to run entire env locally. Anything else is just a sign of bad tooling"
    * "pre-production testing is a best effort verification of a small subset of the guarantees of a system and often can prove to be grossly insufficient for long running systems with protean traffic patterns"
    * "The writing and running of tests is not a goal in and of itself — EVER. We do it to get some benefit for our team, or the business"
    * "there are coverage based fuzzers like afl as well as tools like the address sanitizer, thread sanitizer, memory sanitizer, undefined behavior sanitizer and the leak sanitizer to name a few."
    * "This was but one example of a system that didn’t stand much to benefit from integration testing and where monitoring has worked much better."


#### Why unit tests ? [PP-Chapt34]
- build trust in your code
- build regression tests, helpful for later refactoring
- show examples of how to use your code
- explicitely details the code behaviour on corner cases

### Code review > TDD [CRoTDD]
cf. [Comparing the Defect Reduction Benefits of Code Inspection and Test-Driven Development] & [Why code review beats testing: evidence from decades of programming research]
* You **need** TDD !! (or at least some kind of automated systematic testing) [QETDDM]
* TDD: automated, easy to follow, autonomously done
* CR: increase code quality & reduce defect rate, mutual learning, feeling better (get team mates attention + share responsability -> team building) - For a introductory presentation: [CRTP]
* Do it well: use proper tools, including automated static analysis (findbugs, ArtisticStyle for C/C++/Java, checkstyle + [Cyclomatic]), syntax-checkers...); make it part of the process; detail purpose & testing; track CR ids in commits; no meeting -> can be done at anytime; make it constructive, informal & fun
* cf. [Best practices for code review] [PreMergeCodeReviews]
* [How to Do Code Reviews Like a Human]:
  1. Let computers do the boring parts
  2. Settle style arguments with a style guide
  3. Start reviewing immediately
  4. Start high level and work your way down
  5. Be generous with code examples
  6. Never say “you”
  7. Frame feedback as requests, not commands
  8. Tie notes to principles, not opinions

#### Code reviews guidelines (from @scharrier)
Pour tout le monde
- je fais preuve d’empathie
- je reste humble
- je ne suis pas ironique
- je n’insulte pas

Je suis reviewer:
- je ne suis pas directif
- je suis explicite
- je montre le positif

Je suis reviewé:
- je suis reconnaissant
- je ne prends pas pour moi
- j’explique mes choix
- je réponds à tout
- je n’abandonne pas

Vous n’êtes pas d’accord ?
Discutez de visu, ou demandez à un tiers.

In fine, celui qui maintient DÉCIDE,
Quitte à refaire une PR après.

cf. https://speakerdeck.com/scharrier/code-review-devfest-nantes

+ [A Guide to Naming Variables] : "minimize distance and boilerplate : as coders our job is to communicate to human readers, not computers."
+ [11 proven practices for more effective, efficient peer code review](https://www.ibm.com/developerworks/rational/library/11-proven-practices-for-peer-review/)
+ [Best Kept Secrets of Peer Code Review](https://smartbear.com/SmartBear/media/pdfs/best-kept-secrets-of-peer-code-review.pdf)


## Functional programming
cf. [Functional Programming Patterns]
- _"Don't trust the name - trust the signature"_
- "Domain modelling pattern" : use types to represent constraints, _avoid "primitive obsession"_
- Tail Call Optimization (TCO) : sometimes implemented with a _trampoline_ design pattern


## Fun quotes
- Tony Hoare null "billion-dollar mistake"
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
