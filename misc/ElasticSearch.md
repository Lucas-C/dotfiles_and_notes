http://elasticsearch-cheatsheet.jolicode.com/
http://makina-corpus.com/blog/metier/2015/elasticsearch-tips-and-best-practices-part-1
- use a client library
- use index aliases instead of index names
- use the bulk API
- use explicit mappings
- aggregate field and explicit search field
- asynchronus indexation

## Useful plugins / tools
- http://bigdesk.org/v/2.4.0/#nodes
- plugin marvel (> plugin head)

## Config recommandations
cf. https://www.loggly.com/blog/nine-tips-configuring-elasticsearch-for-high-performance/

    bootstrap.mlockall: true
    # disable memory swapping, BUT may not be allowed by OS -> check if applied with curl http://localhost:9200/_nodes/process?pretty

    action.disable_delete_all_indices: true
    # safer, disallow curl -XDELETE 'http://localhost:9200/*/'

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
    curl 'http://localhost:9200/_nodes?settings&pretty'
    curl 'http://localhost:9200/_aliases?pretty' # get index list
    curl 'http://localhost:9200/$index/_mapping?pretty' # get list of types
    curl 'http://localhost:9200/_cat/shards?pretty' # shards status
    curl 'http://localhost:9200/_river/_search?pretty&q=*' # list rivers

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
