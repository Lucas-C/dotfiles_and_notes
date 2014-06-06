# Memory caching system
memcached

    redis-cli ping
    redis-cli -h HOST -p PORT -n DATABASE_NUMBER llen QUEUE_NAME
    redis-cli -h HOST -p PORT -n DATABASE_NUMBER keys \*

# Queues
- mkfifo, man mq_overview : POSIX queues - not fully implemented : can't read/write on them with shell cmds, need C code
- D-Bus : unix message bus system, with bindings in Java, Python...
- beanstalkd : KISS fast work queue, with lots of existing tools & libs in various languages
- ActiveMQ, RQ(Redis), RestMQ(Redis), RabittMQ : Message queues using AMPQ
- Celery/Kombu : Framework to use any of the above ones - note: Celery using 100% CPU is OK say developpers
- Nameko : python framework for building service orientated software
- fritzy/thoonk.js / fritzy/thoonk.py : Persistent and fast push feeds, queues, and jobs

# DBs
![](https://raw.githubusercontent.com/cockroachdb/cockroach/master/resources/doc/sql-nosql-newsql.png "SQL - NoSQL - NewSQL Capabilities")

- BerkeleyDB, SQLite, LMDB, LevelDB # embedded database
- cockroachdb/cockroach # NewSQL
- MariaDB / Percona / Drizzle # https://blog.mozilla.org/it/2013/03/08/different-mysql-forks-for-different-folks/

# Storage layer for numeric data series over time
RRDtool (the ancestor) and its followers:

- RRDCached
- Graphite Whisper
- OpenTSDB
- reconnoiter
- chriso/gauged

# MySQL / SQLite

LIKE >faster> REGEXP

Unless using --skip-auto-rehash,-A **tab-completion** aka 'automatic rehashing' is enabled on database and table names.

    -- {..} /*...*/ # comments

    sqlite3 places.sqlite "select b.title, b.type, b.parent, a.url from moz_places a, moz_bookmarks b where a.id=b.fk;" # no cmd => interactive - Firefox, type: 1 => bookmark/folder, 2 => tag
    sqlite3 extensions.sqlite 'select id, optionsURL from addon;' # Firefox extensions

    .help
    .tables
    .schema moz_places
    pragma table_info(moz_places)

    mysql -h $HOST -u $USER -p [--ssl-ca=$file.pem] DBNAME -e 'cmd ending with ; or \G' # default port 3306
    mytop # watch mysql

    show tables;
    show table status;
    show columns from $table; # or just: desc $table
    show create table $table;
    show processlist;
    kill $thread_to_be_killed;

## How to start a file to make it executable AND runnable with mysql < FILE.mysql
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
