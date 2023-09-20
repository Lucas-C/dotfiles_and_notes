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
- [Things You Should Know About Databases](https://architecturenotes.co/things-you-should-know-about-databases/)


## Memory caching system
DO NOT "underestimate the complexities and issues caching brings along with it" : [You're probably wrong about caching](http://msol.io/blog/tech/youre-probably-wrong-about-caching/)

[AWS Recos: Caching challenges and strategies](https://aws.amazon.com/fr/builders-library/caching-challenges-and-strategies/)

write-through VS write-around VS write-back caching policies (with Python) : https://shahriar.svbtle.com/Understanding-writethrough-writearound-and-writeback-caching-with-python

[cachegrand](https://github.com/danielealbano/cachegrand): a modern OSS Key-Value store built for today's hardware

JCache API caching strategies (https://dzone.com/refcardz/java-caching):

  FACTOR                  |  STRATEGY
------------------------- | ---------------------------------------
 Cache topology           | Standalone, Distributed, Replicated
 Cache modes              | Embedded cache or Isolated cache
 Transparent cache access | Read-Through and Write-Through caching
 Cache data quality       | Expiry / Eviction policy fine tuning

[Cache stampede](https://en.wikipedia.org/wiki/Cache_stampede): a type of cascading failure that can occur when massively parallel computing systems with caching mechanisms come under very high load

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

dragonfly # modern replacement for Redis and Memcached - Reddit prefers Redis though: https://redis.com/blog/redis-architecture-13-years-later/

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

#### DynamoDB

[The Three AWS DynamoDB Limits You Need to Know](https://www.alexdebrie.com/posts/dynamodb-limits/):
    the item size limit; the page size limit for Query and Scan operations; and the partition throughput limits.

ddbsh is an interactive shell for AWS DynamoDB: https://hypecycles.com/2023/01/25/hello-dynamodb-shell/

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

[Write-Ahead Logging](https://sqlite.org/wal.html) aka `PRAGMA journal_mode=WAL;`:

> - WAL is significantly faster in most scenarios.
> - WAL provides more concurrency as readers do not block writers and a writer does not block readers. Reading and writing can proceed concurrently.
> - Disk I/O operations tends to be more sequential using WAL.

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

[Sharding Pinterest: How we scaled our MySQL fleet](https://medium.com/pinterest-engineering/sharding-pinterest-how-we-scaled-our-mysql-fleet-3f341e96ca6f)

[vitess](https://github.com/vitessio/vitess): database clustering system for horizontal scaling of MySQL through generalized sharding.
Core component of GitHub & YouTube's infrastructure.

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


### Migration methods & tools

[Evolutionary Database Design by Martin Fowler](https://martinfowler.com/articles/evodb.html) - Best practices:
* DBAs collaborate closely with developers
* All database artifacts are version controlled with application code
* All database changes are migrations
* Everybody gets their own database instance
* Developers continuously integrate database changes
* A database consists of schema and data
* All database changes are database refactorings
* Automate the refactorings
* Developers can update their databases on demand
* Clearly separate all database access code
* Release frequently

[Database Refactoring](https://databaserefactoring.com) patterns:
* **Architecture Refactoring**: Add CRUD Methods, Add Mirror Table, Add Read Method, Encapsulate Table With View, Introduce Calculation Method, Introduce Index, Introduce Read Only Table, Migrate Method From Database, Migrate Method To Database, Replace Method(s) With View, Replace View With Methods(s), Use Official Data Source
* **Structural Refactoring**: Drop Column, Drop Table, Drop View, Introduce Calculated Column, Introduce Surrogate Key, Merge Columns, Merge Tables, Move Column, Rename Column, Rename Table, Rename View, Replace LOB With Table, Replace Column, Replace One-To-Many With Associative Tables, Replace Surrogate Key With Natural Key, Split Column, Split Table
* **Data Quality Refactoring**: Add Lookup Table, Apply Standard Codes, Apply Standard Type, Consolidate Key Strategy, Drop Column Constraint, Drop Default Value, Drop Non Nullable, Introduce Column Constraint, Introduce Common Format, Introduce Default Value, Make Column Non Nullable, Move Data, Replace Type Code With Property Flags
* **Referential Integrity Refactoring**: Add Foreign Key Constraint, Add Trigger for Calculated Column, Drop Foreign Key Constraint, Introduce Cascading Delete, Introduce Hard Delete, Introduce Soft Delete, Introduce Trigger for History
* **Transformation**: Insert Data, Introduce New Column, Introduce New Table, Introduce View, Update Data
* **Method Refactoring**: Parameterize Methods, Remove Parameter, Rename Method, Reorder Parameters, Replace Parameter with Explicit Methods, Consolidate Conditional Expression, Decompose Conditional, Extract Method, Introduce Variable, Remove Control Flag, Remove Middle Man, Replace Literal with Table Lookup, Replace Nested Conditional with Guard Clauses, Split Temporary Variable, Substitute Algorithm

> The general rule of thumb is that you make database changes independent of code changes,
> and you always make the changes in such a way that they are compatible with the current deployed code
> AND with the next version that you plan to roll out.
Source: https://news.ycombinator.com/item?id=11481593

[Best Practices using Flyway for Database Migrations (2018)](https://dbabulletin.com/index.php/2018/03/29/best-practices-using-flyway-for-database-migrations/) (also applies to many other tools):
* Team Arrangement and Branching with Flyway: in case _Multiple Developers Make DB Changes_:
    1. Each developer should work with his/her own database copy
    2. Each developer should work in his/her own branch
    3. Use timestamps for delta file versions instead of integers
    4. Enable out of order migrations
    5. Use continuous integration DB environment to merge all DB changes
    6. Do a DB code review before merging changes to CI environment (trunk)
    7. If feasible, combine multiple changes from different branches into one delta file
* Idempotent delta scripts
* Baseline
* Flyway Configuration using Spring Boot
* Flyway and H2 Unit Tests
* Versioned and Repeatable Migrations
> Repeatable migrations are useful in the following situations:
> * Rebuilding indexes, views and stored procedures.
> * Adding permissions
> * Other maintenance tasks
* Dealing with Hotfixes
* Multiple Instances with Flyway
* Manage Multiple Schemes or Shards with Flyway
* Flyway in Production:
    1. make sure you **baseline your production database**
    2. **disable the Clean command**
    3. **enable out-of-order migrations** to allow hotfixes
    4. consider a **dedicated connection string** for your Flyway migrations
    5. decide if **your application will trigger Flyway migrations**, or your DBA will run it manually from command line
* Dry Runs
* Rollback of Flyway Migrations
* Flyway Log

#### FlyWay

https://flywaydb.org/

> With Flyway all changes to the database are called **migrations**. Migrations can be either versioned or repeatable. Versioned migrations come in 2 forms: regular and undo.
> By default, Flyway always wraps the execution of an entire migration within a **single transaction**.

* **Project maturity/community : high** - créé en 2010 - 6.5k GitHub ⭐ - 3000+ commits - 100+ contributeurs
* CLI : `flyway` - Installable comme package NPM : https://www.npmjs.com/package/node-flywaydb
* stocke des métadonnées en base dans une table `flyway_schema_history`

Example: `V1__Initial_version.sql`
```sql
CREATE TABLE car (
    id INT NOT NULL PRIMARY KEY,
    license_plate VARCHAR NOT NULL,
    color VARCHAR NOT NULL
);
ALTER TABLE owner ADD driver_license_id VARCHAR;
INSERT INTO brand (name) VALUES ('DeLorean');
```

**Important notes / limitations** : https://flywaydb.org/documentation/command/undo#important-notes

> Undo migrations assume the whole migration succeeded and should now be undone. - Note (Lucas) : avec PostGreSQL les transactions
> [...] an alternative approach could be to **maintain backwards compatibility between the DB and all versions of the code currently deployed in production**.
> This way the old version of the application is still compatible with the DB, so you can simply roll back the application code, investigate, and take corrective measures.

⛔ La fonctionnalité undo est payante ! 😔

#### LiquiBase

https://docs.liquibase.com

* **Project maturity/community : high** - créé en 2012 - 3.1k GitHub ⭐ - 10000+ commits - 100+ contributeurs
* CLI : `liquibase`
* stocke des métadonnées en base dans des tables `DATABASECHANGELOG` & `DATABASECHANGELOGLOCK`
* supporte des **préconditions**, intègre des **quality checks** sur les migrations rédigées et permet de générer des **diffs**
* [Best Practices Using Liquibase & usage with SpringBoot](https://reflectoring.io/database-migration-spring-boot-liquibase/#best-practices-using-liquibase)
* le changelog peut être au format SQL, XML, JSON ou YAML :

Example: `changelog`
```sql
--liquibase formatted sql

--changeset nvoxland:1
create table test1 (
    id int primary key,
    name varchar(255)
);
--rollback drop table test1;

--changeset nvoxland:2
insert into test1 (id, name) values (1, ‘name 1′);
insert into test1 (id,  name) values (2, ‘name 2′);

--changeset nvoxland:3 dbms:oracle
create sequence seq_test;
```

#### Knex.JS

http://knexjs.org/

> **Migrations** allow for you to define sets of schema changes so upgrading a database is a breeze.
> Migrations use a `knexfile.js`, which specify various configuration settings for the module.
> Migrations are performed inside transactions.

* **Project maturity/community : high** - créé en 2013 - 15k GitHub ⭐ - 2900+ commits - 100+ contributeurs
* CLI : `knex migrate:make $migration_name`
* stocke des métadonnées en base dans une table `knex_migrations`

Example: `knexfile.js`
```javascript
exports.up = function(knex) {
  return knex.schema
    .createTable('users', function (table) {
       table.increments('id');
       table.string('first_name', 255).notNullable();
       table.string('last_name', 255).notNullable();
    })
    .createTable('products', function (table) {
       table.increments('id');
       table.decimal('price').notNullable();
       table.string('name', 1000).notNullable();
    });
};
exports.down = function(knex) {
  return knex.schema
      .dropTable("products")
      .dropTable("users");
};
```

**Limitations** : pas de support pour les indexs full-text (issue #203) ni pour la modifications d'enums (issue #1699)

#### Sequelize

https://sequelize.org/docs/v6/other-topics/migrations/

> A **Migration** in Sequelize is javascript file which exports two functions, up and down, that dictate how to perform the migration and undo it.
> You define those functions manually, but you don't call them manually; they will be called automatically by the CLI.

* **Project maturity/community : high** - créé en 2011 - 26k GitHub ⭐ - 9000+ commits - 100+ contributeurs
* CLI : `npx sequelize-cli db:migrate`
* stocke des métadonnées en base dans une table `SequelizeMeta`

Example: `XXXXXXXXXXXXXX-demo-user.js`
```javascript
```

**Limitations** :

* quelques limitations sont décrites ici, mais ne concernent pas les migrations : https://medium.com/riipen-engineering/limitations-of-sequelize-f131ecf50c3a (2019)
* ne supporte pas AWS Aurora Data API : issue #11021
* performing updates and deletions involving nested objects is currently not possible. For that, you will have to perform each separate action explicitly - issue #11836

#### dbmate

https://github.com/amacneil/dbmate

* **Project maturity/community : medium** - créé en 2016 - 2.5k GitHub ⭐ - 200+ commits - 25 contributeurs
* CLI : `dbmate up`
* stocke des métadonnées en base dans une table `schema_migrations`

Example: `db/migrations/20151127184807_create_users_table.sql`
```sql
-- migrate:up
create table users (
  id integer,
  name varchar(255),
  email varchar(255) not null
);

-- migrate:down
drop table users;
```

#### goose

https://github.com/pressly/goose

* **Project maturity/community : medium** - créé en 2013 - 2.5k GitHub ⭐ - 500+ commits - 65 contributeurs
* CLI : `goose up`
* stocke des métadonnées en base dans une table `goose_db_version`

Example: `20170506082420_create_table_posts.sql`
```sql
-- +goose Up
CREATE TABLE post (
    id int NOT NULL,
    title text,
    body text,
    PRIMARY KEY(id)
);

-- +goose Down
DROP TABLE post;
```

#### terraform-provider-sql

https://registry.terraform.io/providers/paultyng/sql/latest/docs/resources/migrate

* **Project maturity/community : low** - créé en 2020 - 18 GitHub ⭐ - 44 commits - 1 contributeur
* CLI : `terraform`
* stocke ses métadonnées dans le state Terraform
* les migrations non encore appliquées sont exécutées dans l'ordre où elles apparaisent dans l'IAC

```terraform
resource "sql_migrate" "db" {
  migration {
    up = <<SQL
CREATE TABLE users (
    user_id integer unique,
    name    varchar(40),
    email   varchar(40)
);
SQL
    down = "DROP TABLE IF EXISTS users;"
  }

  migration {
    up   = "INSERT INTO users VALUES (1, 'Paul Tyng', 'paul@example.com');"
    down = "DELETE FROM users WHERE user_id = 1;"
  }
}
```

**Limitation** : le projet semble très peu actif : https://github.com/paultyng/terraform-provider-sql/pull/57
