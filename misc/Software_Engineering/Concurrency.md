!! Asynchrone != Parallel != Concurrent

## References:
- [CC-\w\d+] : Clean Code - Robert C. Martin
- [SDP] : Software Design Philosophy - John Ousterhout
- [PP] : The Pragmatic Programmer - Andrew Hunt & David Thomas

## Basic definitions:
- Bound ressources
- Mutual exclusion
- Starvation
- Deadlock : can happen if mutual exclusion + lock&wait + no preemption + circular wait
- Livelock

## Execution models:
- Producer-Consumer
- Readers-Writers
- Dining Philosophers

## Architecture patterns
- Publish/Subscribe aka message bus.
    * Examples: AMQP, MQTT, DDS, JMS, CORBA (with either push/pull mode)
    * https://encrypted.google.com/books?id=RxsyCBr9eLMC
- MVC. Can be chained, i.e. the view on one layer can be the model of another one
    * Model : abstract data model, has no knowledge of views or controllers
    * View : a way to interpret the model, it subscribes to change in the model and logical events from the controller
    * Controller : control the view and provide the model with new data; publishes events to both the model and the view
- Blackboard aka Tuple Space
    * a forum where consumers & producers can exchange data anonymously & asynchronously.
    * can be though as distributed shared associative memory
    * E.g. JavaSpaces operations: read, write, take (pop), notify (set a notification to occur on a write matching a template)

## Advices
- analyze workflow with a simple UML activity diagram [PP-Chapt18]
- use class invariants to detect whenever objects are in an inconsistent state [PP-Chapt18]
- Keep your concurrency-related code separate from other code. Get your non-threaded code working first. [CC-Chapt13]
- Take data encapsulation at heart; severly limit the access of any data that may be shared [CC-Chapt13]
    => Use copies of data / partition data in independent subsets
- Think about shut-down code early [CC-Chapt13]
- Test your code with quick/slow test doubles, on different platform, with varying machine load, with random tuning parameters (iterations count, threads count...)... Also force failures. [CC-Chapt13]
- If tests ever fail, track down the failure [CC-Chapt13]
- When multi-threading, use monitor-style locking whenever possible [SDP]
- Server-based locking > client-based locking [CC-AppA]


# Java
Built-in parallelism the easy way : ExecutorService

synchronized method/code blocks to handle concurrent access:
- Keep synchronized sections as small as possible
- More than one per class is a code smell !

## Standard classes
- ConcurrentHashMap > HashMap
- ReentrantLock : a lock that can be acquired in one method an released in another
- Semaphore : classic implementation, with lock count
- CountDownLatch : a lock that waits for a number of events before releasing all threads waiting on it

Full list of already existing constructs:

- http://docs.oracle.com/javase/7/docs/api/java/util/concurrent/package-summary.html
- http://docs.guava-libraries.googlecode.com/git-history/release/javadoc/com/google/common/eventbus/package-summary.html
    * @Subscribe
    * @AllowConcurrentEvents
    * DeadEvent
- http://docs.guava-libraries.googlecode.com/git-history/release/javadoc/com/google/common/util/concurrent/package-summary.html
    * Futures.addCallback(ListenableFuture)
    * TimeLimiter
    * AtomicDouble

std Atomic* class references > volatile

lib Fork/Join

Example Java checkpoints (sync points):

1. Thread A creates thread B
2. Thread A performs a 'join' with thread B and B terminates
3. Thread A exits a 'synchronize' block and thread V subsequently enters the same 'synchronize' block
4. Thread A writes to a volatile variable and thread B reads it
5. Placing, retrieving an object in a shared zone

Thread.stop Thread.suspend // DEPRECATED ! Do not use them

Fibers // Simple Lightweight Concurrency
