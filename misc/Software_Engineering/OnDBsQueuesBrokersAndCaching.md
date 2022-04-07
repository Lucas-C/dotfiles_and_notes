On DBs, Queues, Brokers and Caching
===================================

<!-- To update this Table Of Contents:
    markdown-toc --indent "    " --maxdepth 3 -i OnDBsQueuesBrokersAndCaching.md
-->

<!-- toc -->

    * [References](#references)
    * [Memory caching system](#memory-caching-system)
        + [memcached](#memcached)
        + [Redis](#redis)
        + [etcd](#etcd)
    * [Queues](#queues)
    * [Storage layer for numeric data series over time](#storage-layer-for-numeric-data-series-over-time)
        + [Graphite](#graphite)
    * [DBs](#dbs)
        + [NoSQL DBs](#nosql-dbs)
        + [SQL DBs](#sql-dbs)

<!-- tocstop -->

## References
- [AOSA_NoSQL] : [The Architecture of Open Source Applications](http://www.aosabook.org) chapter dedicated to NoSQL


## Memory caching system
DO NOT "underestimate the complexities and issues caching brings along with it" : [You're probably wrong about caching](http://msol.io/blog/tech/youre-probably-wrong-about-caching/)

[AWS Recos: Caching challenges and strategies](https://aws.amazon.com/fr/builders-library/caching-challenges-and-strategies/)

write-through VS write-around VS write-back caching policies (with Python) : https://shahriar.svbtle.com/Understanding-writethrough-writearound-and-writeback-caching-with-python

JCache API caching strategies (https://dzone.com/refcardz/java-caching):

  FACTOR                  |  STRATEGY
------------------------- | ---------------------------------------
 Cache topology           | Standalone, Distributed, Replicated
 Cache modes              | Embedded cache or Isolated cache
 Transparent cache access | Read-Through and Write-Through caching
 Cache data quality       | Expiry / Eviction policy fine tuning

### memcached

- for deployment scaling: facebook/mcrouter + http://pdos.csail.mit.edu/6.824-2013/papers/memcache-fb.pdf
- use a firewall !! -> beware security issues: http://www.slideshare.net/sensepost/cache-on-delivery
- `mcsauna` : track the hottest keys on your memcached instances, reporting back in a graphite-friendly format
- https://github.com/Orange-OpenSource/bmc-cache : in-kernel memcache based on eBPF, improves throughput up to 18x
- commands: https://github.com/memcached/memcached/wiki/Commands - Ex:

    echo flush_all | nc $memcache_host $port

### Redis

- builtin datastructures: list, hash, set, sorted set, [hyperloglog](http://antirez.com/news/75)
- easy-as-a-pie pubsub with Python
- **MULTI** allows to combine multiple operations atomically & consistently, and **WATCH** allows isolation. [AOSA]

    redis-cli -h HOST -p PORT -n DATABASE_NUMBER info [keyspace|memory|...]
    redis-cli ping
    redis-cli monitor  # log every command received by Redis, very useful for debugging
    redis-cli llen QUEUE_NAME
    redis-cli keys \*

    maxmemory 2mb
    maxmemory-policy noeviction # Or LRU... - cf. https://redis.io/topics/memory-optimization#memory-allocation

sripathikrishnan/redis-rdb-tools: parse Redis dump.rdb files, Analyze Memory, and Export Data to JSON

    # identify the largest 100 keys in a dump
    rdb -c memory dump_56379.rdb --largest 100 -f largest.csv

twitter/twemproxy # fast, light-weight proxy for memcached and Redis
psobot/till # cache server for immutable, time-limited object storage providing a HTTP interface
bee-queue # fast & robust job/task queue for Node.js, like Celery for Python

https://www.compose.com/articles/how-to-talk-raw-redis/

### etcd

> an open-source distributed key value store, HTTP-based and using Raft, for shared configuration and service discovery. Also: [python-etcd](https://github.com/jplana/python-etcd)

    ./etcdctl set /foo/bar "Hello world" --ttl 10
    $ curl -L -X PUT http://127.0.0.1:4001/v2/keys/message -d value="Hello"
    {"action":"set","node":{"key":"/foo/bar","value":"Hello world","modifiedIndex":4,"createdIndex":4}}

Also: SSD caching, eg. [stec-inc/EnhanceIO][//github.com/stec-inc/EnhanceIO], recommended in [this blog post by JMason](//swrveengineering.wordpress.com/2014/10/14/how-we-increased-our-ec2-event-throughput-by-50-for-free/)


## Queues
- mkfifo, man mq_overview : POSIX queues - not fully implemented : can't read/write on them with shell cmds, need C code   _
- D-Bus : unix message bus system, with bindings in Java, Python...
- beanstalkd : KISS fast work queue, with lots of existing tools & libs in various languages -> its protocol spec is short & simple to read & understand
  The deamon keeps the jobs states: ready (available for workers to pick up) / reserved (beeing processed by a worker) / delayed (waiting N seconds before being ready) / buried (failed & queued for debug)
  Worker processes TCP-connect dialog with it to pick up & execute jobs: either in the "default" tube (= channel / queue) or only jobs put in specific tubes watched
- ActiveMQ, RabbitMQ : Message queues using AMPQ - For Redis based queues, check antirez/disque before RQ or RestMQ
  * [Key metrics for RabbitMQ monitoring](https://www.datadoghq.com/blog/rabbitmq-monitoring/)
- Celery/Kombu : Framework to use any of the above ones - note: Celery using 100% CPU is OK say developpers - Monitoring: mher/flower -
celery_once : prevent multiple execution and queuing of tasks
- Nameko : Python framework for building service orientated software, includes an implementation of RPC over AMQP
- fireworq : lightweight, high-performance job queue system, based on MySQL
- NSQ : distributed and decentralized messaging platform, written in Go (with Python lib available), agnostic to the message format (JSON, MSgPack, protocol buffers... are supported)
- [Dead Letter Queue](https://en.wikipedia.org/wiki/Dead_letter_queue) pattern: store "failing" messages that could not be processed, for several potential reasons

Some queues property from [Redis author](http://antirez.com/news/78):
- at-most-once / at-least-once delivery property
- guaranteed delivery to a single worker at least for a window of time
- best-effort checks to avoid to re-delivery a message after a timeout if the message was already processed
- handle, during normal operations, messages as a FIFO
- auto cleanup of the internal data structures
- [AWS Recos: Avoiding insurmountable queue backlogs](https://aws.amazon.com/fr/builders-library/avoiding-insurmountable-queue-backlogs/)


## Storage layer for numeric data series over time
RRDtool (the ancestor) and its followers:

- RRDCached
- Graphite Whisper
- OpenTSDB
- reconnoiter
- chriso/gauged

Visualization :

- Grafana
- Graphitus
- Facette

### Graphite
It consists of three software components:
- `carbon`: a high-performance service that listens for time-series data (Python)
Alternatives: [carbon-c-relay](https://github.com/grobian/carbon-c-relay), [approved by Justin Mason](http://taint.org/2014/01/27/235802a.html)
- `whisper`: a simple database library for storing time-series data.
Alternatives: [level-tsd](https://github.com/InMobi/level-tsd) -> [LevelDB based backend for Graphite](https://www.inmobi.com/blog/2014/01/24/extending-graphites-mileage)
- `graphite-web`: Graphite's user interface & API for rendering graphs and dashboards

Other tools:
- complete rewrite in Java, with storage in Apache Cassandra, but compatible: http://cyanite.io
- [Gruffalo](https://github.com/outbrain/gruffalo) is an asynchronous Netty based graphite proxy. It protects Graphite from the herds of clients by minimizing context switches and interrupts; by batching and aggregating metrics.
- modern replacement, including multi-dimensional metrics: https://prometheus.io

## DBs
![](https://raw.githubusercontent.com/cockroachdb/cockroach/master/resources/doc/sql-nosql-newsql.png "SQL - NoSQL - NewSQL Capabilities")

The CAP theorem: Consistency, Availability, and Partition tolerance, pick at most two.
First proposed by Eric Brewer in 1998, then proved by Gilbert and Lynch. See also ACID, BASE & [AOSA_NoSQL]
=> Daniel Abadi suggested a more nuanced classification system, PACELC
=> also: [The CAP theorem is too simplistic and too widely misunderstood to be of much use for characterizing systems](https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html)

[nocodb](https://github.com/nocodb/nocodb): Open Source Airtable Alternative, turns any MySQL, PostgreSQL, SQL Server, SQLite & MariaDB into a smart-spreadsheet

### NoSQL DBs

![](http://martinfowler.com/bliki/images/polyglotPersistence/polyglot.png)

- E.g. MongoDB, CouchDB, Riak, Redis, Gizzard... cf. [AOSA_NoSQL]
and the Elder Ones: BigTable ~ HBase, Amazon Dynamo ~ Voldemort, + Cassandra which takes inspiration from both.
- more BerkeleyDB, SQLite, LMDB, RocksDB > LevelDB # embedded database
- cockroachdb/cockroach # NewSQL

spotify/sparkey : simple constant key/value storage library, for read-heavy systems with infrequent large bulk inserts,
    inspired by CDB and Tokyo Cabinet : https://labs.spotify.com/2013/09/03/sparkey/

[The Three DynamoDB Limits You Need to Know](https://www.alexdebrie.com/posts/dynamodb-limits/):
    the item size limit; the page size limit for Query and Scan operations; and the partition throughput limits.



#### MongoDB

    show dbs
    show collections
    db.collec.stats()
    db.collec.find({})
    db.collec.count({})
    db.collec.remove({})
    db.getCollectionNames().forEach(c => db[c].drop())

https://github.com/voyages-sncf-technologies/hesperides/blob/develop/mongo_create_collections.js :

    ['module', 'platform', 'techno'].forEach(c => {
        printjson(db.createCollection(c, {collation: {locale: 'fr', strength: 2}}))
        printjson(db[c].createIndex({key: 1}))
        print(c, 'indexes:')
        printjson(db[c].getIndexes())
    })

Mongo shell: !! it connects to the 1st node of the connexion URI, even if it is not a primary.
To allow executing commands on a non-primary node:

    node:SECONDARY> rs.slaveOk()


### SQL DBs

https://blog.jooq.org/2016/07/05/say-no-to-venn-diagrams-when-explaining-joins/

LIKE >faster> REGEXP

    -- {..} /*...*/ # comments


#### PostgreSQL
[Meta-Commands](http://www.postgresql.org/docs/current/interactive/app-psql.html#APP-PSQL-META-COMMANDS)

    \? # and \h $cmd
    \dt+ # list tables - There are many other \d... commands
    \x auto # expanded display mode - \x on for v<9.2

Temporary instances for unit-testing: http://faitout.fedorainfracloud.org

[PostgreSQL Features You May Not Have Tried But Should](https://pgdash.io/blog/postgres-features.html):
- Pub/Sub Notifications
- Table Inheritance
- Foreign Data Wrappers: virtual tables that actually serve data from another PostgreSQL instance, or even SQLite files, MongoDB, Redis, and more
- Partitioned Tables : sharding of a table into multiple child tables, based on a partition key.
This allows a single, large table to be physically stored as separate tables, for better DML performance and storage management.
- Range Types
- Array Types
- Triggers : execute a specific function when rows are inserted, updated or deleted from a table
- pg_stat_statements : this extension records a wealth of information about each statement executed, including the time taken, the memory used and disk I/Os initiated
- other index types : B-Tree, Hash, GIN, BRIN
- Full Text Search
- pgmetrics & pgDash : monitoring


#### SQL*PLus

    # in login.sql
    SET TIMING ON
    SET SERVEROUTPUT ON
    SET LINESIZE 180 PAGESIZE 1000


#### SQLite

[DB browser for SQLite](https://sqlitebrowser.org)

https://remusao.github.io/posts/2017-10-21-few-tips-sqlite-perf.html

    sqlite3 extensions.sqlite 'select id, optionsURL from addon;' # Firefox extensions
    sqlite3 cookies.sqlite 'select name,value,path,expiry,creationTime from moz_cookies where name = "PHPSESSID";'   #_
    sqlite3 places.sqlite "SELECT b.title, b.type, b.parent, a.url FROM moz_places AS a, moz_bookmarks AS b WHERE a.id=b.fk;" # Firefox, type: 1 => URL, 2 => tag/folder
    SELECT folder.title, COUNT(bookmark.id) FROM moz_bookmarks AS folder, moz_bookmarks AS bookmark WHERE bookmark.parent=folder.id AND folder.parent!=4 GROUP BY folder.title; # List only folders. folder.parent=4 => tag

    .help
    .tables
    .schema moz_places
    pragma table_info(moz_places)
    #_ Display columns:
    .mode column
    .headers on

[Towards Inserting One Billion Rows in SQLite Under A Minute](https://avi.im/blag/2021/fast-sqlite-inserts/) via https://sebsauvage.net/links/?DYeYQw

    PRAGMA journal_mode = OFF;
    PRAGMA synchronous = 0;
    PRAGMA cache_size = 1000000;
    PRAGMA locking_mode = EXCLUSIVE;
    PRAGMA temp_store = MEMORY;

[The ultimate SQLite extension set](https://antonz.org/sqlean/):

* **crypto**: cryptographic hashes like MD5 or SHA-256.
* **fileio**: read and write files and catalogs.
* **fuzzy**: fuzzy string matching and phonetics.
* **ipaddr**: IP address manipulation.
* **json1**: JSON functions.
* **math**: math functions.
* **re**: regular expressions.
* **stats**: math statistics — median, percentiles, etc.
* **text**: string functions.
* **unicode**: Unicode support.
* **uuid**: Universally Unique IDentifiers.
* **vsv**: CSV files as virtual tables.


#### MySQL
[5 subtle ways you're using MySQL as a queue, and why it'll bite you](https://blog.engineyard.com/2011/5-subtle-ways-youre-using-mysql-as-a-queue-and-why-itll-bite-you)

MariaDB / Percona / Drizzle # https://blog.mozilla.org/it/2013/03/08/different-mysql-forks-for-different-folks/

Unless using --skip-auto-rehash,-A **tab-completion** aka 'automatic rehashing' is enabled on database and table names.

[Unix SSH Auth](http://www.mon-code.net/article/72/utiliser-le-compte-linux-pour-se-connecter-de-facon-securise-a-mariadb-et-mysql-sans-mot-de-passe)

[REST API for v>5.7](www.infoq.com/news/2014/09/MySQL-REST)

[MyWebSQL web admin UI](http://freedif.org/mywebsql-web-based-database-administration-panel/)

[Why Uber Engineering Switched from Postgres to MySQL](https://eng.uber.com/mysql-migration/)

[vitess](https://github.com/vitessio/vitess): database clustering system for horizontal scaling of MySQL through generalized sharding.
Core component of GiThub & YouTube's infrastructure.

    mysqladmin --defaults-file=/etc/mysql/debian.cnf status # mysqladmin config file can be found in /etc/init.d/mysql, along MySQL own one: /etc/mysql/my.cnf

    cd $MYSQL_BASE_DIR
    bin/mysql_install_db --datadir=$OLDPWD/data
    bin/mysqld_safe --datadir=$OLDPWD/data &   #_
    bin/mysql test < db-dump.sql

    mysql -h $HOST -u $USER -p [--ssl-ca=$file.pem] DBNAME -e "$query" # default port 3306
    mytop # watch mysql
    mysqlslap # benchmarks, load emulation & stress testing

    SHOW databases;
    SHOW tables;
    SHOW table status;
    SHOW columns FROM $table; -- or just: DESC $table
    SHOW create table $table;
    SHOW processlist;
    KILL $thread_to_be_killed;
    DESLECT user, host FROM mysql.user\G -- instead of ";" => enable pretty-print

Human-readable dump by shortening the 'INSERT' statements:

    perl -pe 's/^(INSERT INTO .*? VALUES).*/\1 .../' $dump.sql | less  # using perl because of its non-greedy wildcar match

Log all queries in mysql without restart (FROM: http://stackoverflow.com/questions/303994/log-all-queries-in-mysql/20485975#20485975)

    SET global log_output = 'FILE';
    SET global general_log_file='/Applications/MAMP/logs/mysql_general.log';
    SET global general_log = 1;

Stop the Windows service (e.g. installed with MySQL Workbench):

    sc interrogate MySQL57
    sc stop MySQL57


##### How to start a file to make it executable AND runnable with mysql < FILE.mysql

    /*/cat <<NOEND | mysql #*/
    USE ...;
    WITH
        subquery AS ( SELECT ... ),
        ...
    SELECT
        id, name
    FROM
        subquery,
        ... # "inline" SELECT are also allowed
    WHERE
        ...
    ORDER BY
        ...;
