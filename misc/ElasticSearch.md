http://elasticsearch-cheatsheet.jolicode.com/
http://makina-corpus.com/blog/metier/2015/elasticsearch-tips-and-best-practices-part-1
- use a client library
- use index aliases instead of index names
- use the bulk API
- use explicit mappings
- aggregate field and explicit search field
- asynchronus indexation
An ElasticSearch dev talk: https://speakerdeck.com/elasticsearch/maintaining-performance-in-distributed-systems

## Useful plugins / tools
- [curator](https://www.elastic.co/blog/curator-tending-your-time-series-indices) : Python script to perform maintenance tasks, e.g. delete indices by total space consumed or by date
- vagrant-elasticsearch-cluster : Create an ElasticSearch cluster with a simple single bash command
- http://bigdesk.org/v/2.4.0/#nodes
- plugin marvel (> plugin head)

## Config recommandations
How to choose the number of nodes in a cluster: http://blog.overnetcity.com/2014/04/24/elasticsearch-the-split-brain-problem/

5 Lessons Learned From A Year Of Elasticsearch In Production : https://tech.scrunch.com/blog/lessons-learned-from-a-year-of-running-elasticsearch-in-production/

cf. https://www.loggly.com/blog/nine-tips-configuring-elasticsearch-for-high-performance/

    bootstrap.mlockall: true
    # disable memory swapping, BUT may not be allowed by OS -> check if applied with curl http://localhost:9200/_nodes/process?pretty

    action.disable_delete_all_indices: true
    # safer, disallow curl -XDELETE 'http://localhost:9200/*/'

    bootstrap.mlockall: true # prevents the memory from being swapped by the OS

## Aggregates (formerly facets)

Terms Aggregation: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html

    "aggregations" : {
      "agg_name": {
          "terms" : { "field" : "field_name" }
      }
    }

!! Terms aggs are also subjects to "not_analyzed" parsing control

## Java client

    Jest is a great Java client to connect to ELK through HTTP (not with custom protocol on port 9300)

        JestClientFactory factory = new JestClientFactory();
        factory.setHttpClientConfig(new HttpClientConfig
                .Builder(this.elkConfig.getServerUri())
                .multiThreaded(true)
                .build());
        JestClient elasticSearchClient = factory.getObject();

        Search search = new Search.Builder(query)
                .addIndex(indexName)
                .setParameter(Parameters.SIZE, this.elkConfig.getQuerySize())
                .setParameter(Parameters.EXPLAIN, true)
                .build();

        SearchResult elkResult = elasticSearchClient.execute(search);
        List<Map<String, Object>> results = elkResult.getHits(sourceType).stream()
                                                     .map(hit -> hit.source)
                                                     .collect(Collectors.toList());


## Issues experienced

### By default, ELS does NOT provide exact string matching

You need to flag your field as "not_analyzed" : https://www.elastic.co/guide/en/elasticsearch/guide/current/_finding_exact_values.html

This can be set as a default for all string fields: http://stackoverflow.com/a/27571721

!! Defining a mapping for a unique field will deactivate ALL dynamic mapping

### "SearchPhaseExecutionException[Failed to execute phase [query_fetch], all shards failed]"

- root cause: unknown, but the following showed some issues: http://localhost:8080/nfnsr-es/_cat/shards?pretty
- tested fix: delete & recreate the index:

    curl -XDELETE "$host:$port/nfnsr-es/$index"
    curl -XPUT "$host:$port/nfnsr-es/$index"


## Useful curl commands

    curl 'http://$host:$port/$index/_search?pretty&size=100' # search all

### Instances qui se synchronisent toutes seules

    discovery.zen.ping.multicast.enabled: false
    # check if enabled with /_nodes?pretty

### Impossible de faire une recherche avec des DateTime

Penser à échaper les ":" qui sont des caractères réservés dans la syntax Lucène : `\\:`

### General status

    curl 'http://localhost:9200/_cluster/health?pretty'
    curl 'http://localhost:9200/_cluster/state?pretty'
    curl 'http://localhost:9200/_nodes?settings&pretty'
    curl 'http://localhost:9200/_aliases?pretty' # get index list
    curl 'http://localhost:9200/$index/_mapping?pretty' # get list of types
    curl 'http://localhost:9200/_cat/shards?pretty' # shards status
    curl 'http://localhost:9200/_river/_search?pretty&q=*' # list rivers - DEPRACATED
    curl 'http://localhost:9200/_cluster/pending_tasks?pretty'

### Adding content & searching

    curl -XPUT 'http://127.0.0.1:9200/test/book/1' -d '
    {
     "title": "All About Fish",
     "author": "Fishy McFishstein",
     "pages": 3015
    }'
    curl 'http://127.0.0.1:9200/test/book/1'
    curl 'http://127.0.0.1:9200/test/book/_search' -d '
    {
      "query": {
        "filtered": {
          "filter": {
            "term": {
              "author": "Fishy McFishstein"
     }' | jq -r .error//.
    curl 'http://127.0.0.1:9200/_search' -d '
    curl 'http://127.0.0.1:9200/test/book/1/_explain' -d '
    {
      "query": {
        "filtered": {
          "filter": {
            "term": {
              "author": "Fishy McFishstein"
            }
          }
         }
       }
     }' | jq -r .error//.
    curl 'http://127.0.0.1:9200/test/book/_search' -d '
    {
        "query" : {
            "query_string" : {
                "fields": ["author"],
                "query" : "\"Fishy McFishstein\""
            }
        }
    }' | jq -r .error//.
    curl 'http://127.0.0.1:9200/test/book/_search' -d '
    {
      "query": {
        "match" : {
          "author" : "Fishy McFishstein"
        }
      }
    }' | jq -r .error//. # 'match' queries have replaced 'text' ones in  1.0.0.RC1
    curl 'http://127.0.0.1:9200/test/book/1/_explain' -d '
    {
      "query": {
        "filtered": {
          "filter": {
            "term": {
              "author": "Fishy McFishstein"
            }
          }
        }
      }
    }' | jq -r .error//.

_

# Boost example

We use constant score queries to get rid of the default TF/IDF Lucene-based scores,
and hence avoid skewing the end _score.   _

    {
      "query": {
        "bool": {
          "must": [
            {
              "constant_score": {
                "query": {
                  "match": {
                    "type": "job_offer"
                  }
                }
              }
            },
            {
              "constant_score": {
                "query": {
                  "match": {
                    "status": 1.0
                  }
                }
              }
            }
          ],
          "should": [
            {
              "constant_score": {
                "query": {
                  "term": {
                    "field_nsr_all_punchline_selected": "1"
                  }
                },
                "boost": 3.0
              }
            },
            {
              "constant_score": {
                "query": {
                  "term": {
                    "field_nsr_punchline:nid": "1"
                  }
                },
                "boost": 3.0
              }
            }
          ]
        }
      },
      "sort": [
        {
          "_score": {
            "order": "desc"
          }
        },
        {
          "field_nsr_publication_date": {
            "order": "desc"
          }
        }
      ]
    }
