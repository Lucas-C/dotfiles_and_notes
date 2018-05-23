[500 Lines or Less](http://www.aosabook.org)
============================================

::: toc
[[toc]]
:::

[A Simple Object Model](http://aosabook.org/en/500L/a-simple-object-model.html) by Carl Friedrich Bolz
-> compare method-based model (like Smalltalk, Ruby, and JavaScript) with attribute-based models (like Lua and Python, which explain what are "bound methods")
+ explain "maps" instance optimization used in PyPy and the JS V8 engine, where it is called "hidden classes"
+ explain the core difference between traditionnal Object/Class models and prototype-based languages like JavaScript: the concept of class does not exist and objects instead inherit directly from each other


[The Architecture of Open Source Applications](http://www.aosabook.org) - Amy Brown & Greg Wilson
=================================================================================================
Takeaways


## Asterisk by Russell Bryant


## Audacity by James Crook


## The Bourne-Again Shell by Chet Ramey
- change logs are important
- introduce compatibility levels early, to notify users of non-backward compatible changes


## Berkeley DB by Margo Seltzer & Keith Bostic
- 4 access methods: Btree & Hash support variable-length key/value pairs;
Recno & Queue support record-number/value pairs
(the former with variable length values, the later with fixed-length values only)
- ACID, invented by Jim Gray:
    * Atomicity: all operations performed within a transaction are either all present or all absent of the DB
    * Consistency: a transaction moves the DB from one logically consistent state to another
    * Isolation: from the perspective of a transaction, it is running sequentially zithout any concurrent transaction running
    * Durability: once a transaction is committed, it stays commited

Design lessons:

1. Well defined API boundaries are important
2. Software architecture requires a different mind set from debugging code:
do it separetely, **beforehand**
3. Whether to rewrite / redesign a module is a difficult decision:
you will always upset either the users or the mainteners
4. Consistent naming style is important
5. Choose upgrade battles carefully.
Don't hide them to users, highlight them and make sure they break old code at compile time


## CMake by Bill Hoffman & Kenneth Martin


## Eclipse by Kim Moir
Great versioning naming scheme


## Graphite by Chris David


## The Hadoop Distributed File System by Robert Chansler, Hairong Kuang, Sanjay Radia, Konstantin Shvachko & Suresh Srinivas
OSGI


## Continuous Integration by C. Titus Brown and Rosangela Canino-Koning
- list features & compare architectures of CDash, Pony-build, Jenkins (formerly called Hudson)
- [PubSubHubHub](https://code.google.com/p/pubsubhubbub/) : open, server-to-server webhook-based publish/subscribe protocol


## Jitsi by Emil Ivov


## LLVM by Chris Lattner
- modular design as the key
- automated test case reduction with BugPoint
- highlight the importance of APIs and backward compatibility
- powerful textual LLVM IR


## Mercurial by Dirkjan Ochtman


## The NoSQL Ecosystem by Adam Marcus
- relational DB usually have a "query optimizer" component
- SQL queries limits:
    * complexity leads to unpredictability: difficulty to reason on the cost of each query
    * the relational model may be needlessly restrictive and is not always the best for every problem / kind of data
    * scaling & denormalisation makes a SQL DB closer to a key-value store
- Inspirations: BigTable ~ HBase & Amazon Dynamo ~ Voldemort, + Cassandra which takes inspiration from both.
Other systems mentionned: MongoDB, CouchDB, Riak, Redis, Gizzard
- Characteristics: data & query model, durability, scalability, partitioning, consistency,
transactional semantics, single-server performances, analytical workloads
- Data models: key-value, key-datastructure, key-document, BigTable column families
& graph storage (HyperGraphDB, Neo4j...) & complex queries (multi-properties keys, MapReduce analytical queries...)
- ACID guarantees
    * Atomic : all or none of the operations happen
    * Consistency : the transaction leaves the DB in a consistent, uncorrupted state
    * Isolation : if 2 transactions touch the same record, they will do without stepping on each other's feet
    * Durability : once a transaction is commited, it's stored in a safe place
- NoSQL => application code must be more defensive & future-proof, e.g. resilient to sloppy-schema updates
- Data durability
    * Single-server: _fsync_ calls frequency control, _log_ of sequential update operations
    * Multi-server: master-slave, replicat sets, rack-aware configuration
- scaling: sharding (don't do it until you have to), read-replicas, caching, coordinators, load-balancing,
distributed hash tables aka consistent hash rings, various detailed forms of range-partitionning...
- consistency: strong (R+W>N) & eventual, CAP theorem => system must be partition-tolerant and has either consistency or availability,
Yahoo's PNUTS relaxed consistency & relaxed availability, hinted handoff, Merkle tree, gossip protocol

## Python packaging by Tarek Ziadé
- distutils2 > pip > distribute > setuptools > distutils BUT it has been abandoned :( Check zc.buildout/conda/bento/hashdist/pyinstaller for new projects or keep using setuptools: https://packaging.python.org
- some old distutils issues: `python setup.py --name` may fails; `setup(requires=['ldap'])` is useless; PyPI may act as a SPOF; there is no way to remove installed files (there is `python setup.py install --record` but it is never used); if a dependency install fails or there is a dependency conflicts, the system can end up in a broken state...
- Simple Index protocol and XML-RPC APIs
- `dist-info` metadata of files installed, including a _RESOURCES_ file mapping project-root-relative files to paths in the system (e.g. /etc/, /var/...)
- server mirroring protocol, with strict host naming convention, a CNAME of the last server available, download stats & minimal security
- lessons learned: it's all about PEPs, a pkg that enters the std lib has one foot in the grave & backward compatibility


## Riak and Erlang/OTP by Francesco Cesarini, Andy Gross and Justin Sheehy
- distributed, fault tolerant, open source database offering high-availability and linear scalability of both capacity and throughput
- intro to the Erlang language
- Erland/OTP provides **very** strong resilience to failure: a large entreprise wasn't able to make it crash during stress-testing (§15.7)


## Selenium WebDriver by Simon Stewart
- 3 tools: Selenium IDE (Firefox plugin), Selenium WebDriver (multi-languages APIs), Selenium Grid (allow parallel testing on several machines)
- architectural themes: keep the costs down; emulate the user; prove the drivers work; but you shouldn't need to understand how everything works; lower the bus factor; have sympathy for a javascript implementation; every method call is an RPC call; we are an open-source project.
- "bus factor": the number of key developers who would need to meet some grisly end - presumably by being hit by a bus - to leave the project in a state where it couldn't continue.

    driver.findElement(By.id("some_id"));

Interesting explaination on the reasons & consequences of some core design choices: supporting Firefox Driver tests written in pure Javascript,
avoid the need for an installer for IE Driver, required compatibility with old stable browser versions, Microsoft not allowing to distribute some files, IE COM Interface must be called from a single thread...


## Sendmail by Eric Allman
- originally named `delivermail`, it was just glue to hold the various mail systems together rather than being a mail system in its own right.
- design principles:
    * Accept that One Programmer Is Finite
    * Don't Redesign User Agents
    * Don't Redesign the Local Mail Store
    * Make Sendmail Adapt to the World, Not the Other Way Around
    * Change as Little as Possible
    * Think About Reliability Early
    * Get something working quickly and then enhance working code as needed and as the problem was better understood

> As the debate raged, MTP got more and more complex until in frustration SMTP (Simple Mail Transfer Protocol) was drafted more-or-less by fiat

- On Syslog:

> I would make one specific change: I would pay more attention to making the syntax of logged messages machine parseable—essentially, I failed to predict the existence of log monitoring.


## SnowFlock by Roy Bryant and Andrés Lagar-Cavilla
- VM cloning: "it can be used to create dozens of new VMs in five seconds or less", "because clones inherit the warm [cache] buffers of their parent, they reach their peak performance sooner".
- "SnowFlock consists of a set of modifications to the Xen hypervisor that enable it to smoothly recover when missing resources are accessed, and a set of supporting processes and systems that run in dom0 and cooperatively transfer the missing VM state"
- Uses Copy-on-Write, or CoW memory

> The entire memtap design centers on a page presence bitmap.
> The bitmap is created and initialized when the architectural descriptor is processed to create the clone VM.
> The bitmap is a flat bit array sized by the number of pages the VM's memory can hold.
> Intel processors have handy atomic bit mutation instructions: setting a bit,
> or doing a test and set, can happen with the guarantee of atomicity with respect to other processors in the same box.
> This allows us to avoid locks in most cases, and thus to provide access to the bitmap
> by different entities in different protection domains: the Xen hypervisor, the memtap process, and the cloned guest kernel itself.

- Lesson learned:

> simple and elegant solutions scale well and do not hide unwelcome surprises as load increases.


## SocialCalc by Audrey Tang
- WikiCalc was invented based on the wiki model to circumvent limitations (notably collaboration issues) of existing spreadsheets softwares.
- => useful as a stand-alone server running on localhost, but not very practical to embed as part of web-based content management systems
- SocialCalc is a ground-up rewriteof WikiCalc in Javascript based on some of the original Perl code.
- The initial design had some flaws:
  - requires fast connection between browser & server
  - memory issues when using big grids, starting as soon as 100x100:
- In the new version, the server only serves entire serialized spreadsheets on GET requests (and saving it back to the DB when requested)
- Real-time collaboration: originally implemented with Mozilla/XPCOM & D-Bus/Telepathy,
then extended to work cross-browsers with the Web::Hippie framework (providing JSON-over-WebSocket),
with fallback to web_socket.js Flash emulation of WebSocket if available, and else MXHR (Multipart XML HTTP Request).
- Lessons Learned:
    - Chief Designer with a Clear Vision
    - Wikis for Project Continuity
    - Embrace Time Zone Differences
    - Always Have a Roadmap; Forgiveness > Permission; Remove deadlocks; Seek ideas, not consensus; Sketch ideas with code; Distribute Knwoledge
    - Drive Development with Story Tests


### From SocialCalc to EtherCacl by Audrey Tang
(from _The Performance of Open Source Software_)

> Several shortcomings in SocialCalc performance and scalability characteristics, motivating a series of system­wide rewrites in order to reach acceptable performance.

- used Redis for persistence behind EtherCalc.org
- initial Perl code profiling with NYTProf & DTrace
- Node profiling more difficult, relying on Node Webkit Agent
- load testing using Apache `ab` and Zombie.js for simulating browser-side operations
- found the bottleneck was in jsdom library
- used webworker threads (implementing W3C API)

> EtherCalc was ported through a lineage of four languages: JavaScript, CoffeeScript, Coco and LiveScript.

> LiveScript eliminated nested callbacks with novel constructs such as _backcalls_ and _cascades_.


## Telepathy by Danielle Madeley
"modular framework for real-time communications that handles voice, video, text, file transfer, and so on"
Rely heavily on D-Bus messaging


## Thousand Parsec by Alan Laudicina and Aaron Mavrinac
"Videogame framework for building multiplayer, turn-based space empire strategy games."
What Didn't Work: using a binary protocol -> too cumbersome to debug


## Violet by Cay Horstmann
Lightweight UML editor.
- Uses JavaBeans Properties, XML long-term persistence serialization, Java WebStart, Java 2D, Swing Undo/Redo.
- Uses "convention over configuration".
- Do not wanted to use OSGi, implemented instead "the simplest thing that works":

> Each JAR file must have a subdirectory META-INF/services containing a file whose name is the
> fully qualified classname of the interface (such as com.horstmann.violet.Graph), and that
> contains the names of all implementing classes, one per line. The ServiceLoader constructs a
> class loader for the plugin directory, and loads all plugins:

    ServiceLoader<Graph> graphLoader = ServiceLoader.load(Graph.class, classLoader);
    for (Graph g : graphLoader) // ServiceLoader<Graph> implements Iterable<Graph>
    registerGraph(g);

"This is a simple but useful facility of standard Java that you might find valuable for your own
projects."


## VisTrails by Juliana Freire, David Koop, Emanuele Santos, Carlos Scheidegger, Claudio Silva, and Huy T. Vo
Data exploration and visualization, with similarities with scientific workflow systems such as Kepler and Taverna, and visualization systems such as AVS and ParaView.

- emphasis on tracking provenance
- version tree: change-based provenance
- intermediate workflow steps caching
- serialization, storage & versioning using git
- extensibility with Python modules + support for their upgrade at runtime

> Python is quickly becoming a universal modern glue language for scientific software (2011 !)

- integration in LaTeX & PowerPoint

Lessons learned:

- "The initial feedback and the encouragement we received from these users was instrumental in driving the project forward",
    "most features in the system were designed as direct response to user feedback",
    "being responsive to users does not necessarily mean doing exactly what they ask for"
- not all features have been heavily used, e.g. analogies and the version tree, because they are highly unusual and...
- "we have been much better at developing new features than at documenting the existing ones"
- "VisTrails is a complex tool and requires a steep learning curve for some users"


## VTK by Berk Geveci and Will Schroeder
The Visualization Toolkit (VTK) is a widely used software system for data processing and visualization.

> To really understand a software system it is essential to not only understand what problem it solves, but also the particular culture in which it emerged

- one million LoC of C++
- emphasis on the choice of the license
- language bindings to Python, Java, Tcl and others
- tools: CMake, CDash/CTest, CPack, Doxygen, Mantis (bug tracker)

Lessons learned:

- managing growth: formalized management structures are being created + plans to modularize the toolkit further
- Design Modularity
- Missed Key Concepts
- Design Issues


## Battle For Wesnoth by Richard Shimooka and David White
Turn-based fantasy strategy game.

- 200 000 LoC of C++, using a very modular architecture
- uses the Simple Directmedia Layer (SDL) for video, I/O and event handling,
and also Boost, Pango with Cairo for internationalized fonts, zlib and GNU gettext
- game content defined in Wesnoth Markup Language (WML)
- bindings in Lua for the Game Logic, and Python for the defining an AI

WML:

- dictionary structure, with "include-based" macro system
- caching system
- to allow for completely configurable unit behavior with WML,
the language <cite>would have to be extended into a full-fledged programming language
and that would be intimidating for many aspiring contributors</cite>

Multiplayer Implementation:

> The project simply does not try hard to prevent cheating.
> Deliberately preventing competitive ranking systems on the
> server greatly reduced the motivation for individuals to cheat.

