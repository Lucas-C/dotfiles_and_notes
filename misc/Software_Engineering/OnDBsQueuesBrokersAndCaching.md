## References
- [AOSA_NoSQL] : [The Architecture of Open Source Applications](http://www.aosabook.org) chapter dedicated to NoSQL

## Memory caching system
memcached

- for deployment scaling: facebook/mcrouter + http://pdos.csail.mit.edu/6.824-2013/papers/memcache-fb.pdf
- use a firewall !! -> beware security issues: http://www.slideshare.net/sensepost/cache-on-delivery

_Redis_ **MULTI** allows to combine multiple operations atomically & consistently, and **WATCH** allows isolation. [AOSA]

    redis-cli ping
    redis-cli -h HOST -p PORT -n DATABASE_NUMBER llen QUEUE_NAME
    redis-cli -h HOST -p PORT -n DATABASE_NUMBER keys \*

twitter/twemproxy # fast, light-weight proxy for memcached and Redis

## Queues
- mkfifo, man mq_overview : POSIX queues - not fully implemented : can't read/write on them with shell cmds, need C code
- D-Bus : unix message bus system, with bindings in Java, Python...
- beanstalkd : KISS fast work queue, with lots of existing tools & libs in various languages
- ActiveMQ, RQ(Redis), RestMQ(Redis), RabittMQ : Message queues using AMPQ
- Celery/Kombu : Framework to use any of the above ones - note: Celery using 100% CPU is OK say developpers
- Nameko : python framework for building service orientated software
- fritzy/thoonk.js / fritzy/thoonk.py : Persistent and fast push feeds, queues, and jobs

## Storage layer for numeric data series over time
RRDtool (the ancestor) and its followers:

- RRDCached
- Graphite Whisper
- OpenTSDB
- reconnoiter
- chriso/gauged

## DBs
![](https://raw.githubusercontent.com/cockroachdb/cockroach/master/resources/doc/sql-nosql-newsql.png "SQL - NoSQL - NewSQL Capabilities")

The CAP theorem: Consistency, Availability, and Partition tolerance, pick at most two.
First proposed by Eric Brewer in 1998, then proved by Gilbert and Lynch. See also ACID, BASE & [AOSA_NoSQL]
=> Daniel Abadi suggested a more nuanced classification system, PACELC

- BerkeleyDB, SQLite, LMDB, LevelDB # embedded database
- cockroachdb/cockroach # NewSQL

LIKE >faster> REGEXP

    -- {..} /*...*/ # comments

### SQL*PLus

    # in login.sql
    SET TIMING ON
    SET SERVEROUTPUT ON
    SET LINESIZE 180 PAGESIZE 1000

### SQLite

    sqlite3 extensions.sqlite 'select id, optionsURL from addon;' # Firefox extensions
    sqlite3 places.sqlite "SELECT b.title, b.type, b.parent, a.url FROM moz_places AS a, moz_bookmarks AS b WHERE a.id=b.fk;" # Firefox, type: 1 => URL, 2 => tag/folder
    SELECT folder.title, COUNT(bookmark.id) FROM moz_bookmarks AS folder, moz_bookmarks AS bookmark WHERE bookmark.parent=folder.id AND folder.parent!=4 GROUP BY folder.title; # List only folders. folder.parent=4 => tag

    .help
    .tables
    .schema moz_places
    pragma table_info(moz_places)
    # Display columns:
    .mode column
    .headers on

### MySQL
MariaDB / Percona / Drizzle # https://blog.mozilla.org/it/2013/03/08/different-mysql-forks-for-different-folks/

Unless using --skip-auto-rehash,-A **tab-completion** aka 'automatic rehashing' is enabled on database and table names.

[Unix SSH Auth](http://www.mon-code.net/article/72/utiliser-le-compte-linux-pour-se-connecter-de-facon-securise-a-mariadb-et-mysql-sans-mot-de-passe)

[REST API for v>5.7](www.infoq.com/news/2014/09/MySQL-REST)

    mysqladmin --defaults-file=/etc/mysql/debian.cnf status # mysqladmin config file can be found in /etc/init.d/mysql, along MySQL own one: /etc/mysql/my.cnf

    cd $MYSQL_BASE_DIR
    bin/mysql_install_db --datadir=$OLDPWD/data
    bin/mysqld_safe --datadir=$OLDPWD/data &
    bin/mysql test < db-dump.sql

    mysql -h $HOST -u $USER -p [--ssl-ca=$file.pem] DBNAME -e 'cmd ending with ; or \G' # default port 3306
    mytop # watch mysql
    mysqlslap # benchmarks, load emulation & stress testing

    show databases;
    show tables;
    show table status;
    show columns from $table; # or just: desc $table
    show create table $table;
    show processlist;
    kill $thread_to_be_killed;

#### How to start a file to make it executable AND runnable with mysql < FILE.mysql

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
