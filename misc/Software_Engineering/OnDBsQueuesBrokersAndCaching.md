# Memory caching system
memcached

    redis-cli ping
    redis-cli -h HOST -p PORT -n DATABASE_NUMBER llen QUEUE_NAME
    redis-cli -h HOST -p PORT -n DATABASE_NUMBER keys \*

# Queues
- mkfifo, man mq_overview # POSIX queues - not fully implemented : can't read/write on them with shell cmds, need C code
- beanstalk # lots of existing tools & libs in various languages
- ActiveMQ, RQ(Redis), RestMQ(Redis), RabittMQ # Message queue using AMPQ
- Celery/Kombu # Framework to use any of the above ones - note: Celery using 100% CPU is OK say developpers
- Nameko # python framework for building service orientated software
- fritzy/thoonk.js / fritzy/thoonk.py # Persistent and fast push feeds, queues, and jobs

# DBs
![](https://raw.githubusercontent.com/cockroachdb/cockroach/master/resources/doc/sql-nosql-newsql.png "SQL - NoSQL - NewSQL Capabilities")

- BerkeleyDB, SQLite, LMDB, LevelDB # embedded database
- cockroachdb/cockroach # NewSQL

# Storage layer for numeric data series over time
RRDtool (the ancestor) and its followers:

- RRDCached
- Graphite Whisper
- OpenTSDB
- reconnoiter
- chriso/gauged

