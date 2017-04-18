# aws-lambda-elasticsearch
1. Environment is set up according to [this artile](https://aws.amazon.com/blogs/database/indexing-metadata-in-amazon-elasticsearch-service-using-aws-lambda-and-python/)
2. To get the Elasticsearch packages, run:
```
pip install requests -t /path/to/project-dir
pip install Elasticsearch -t /path/to/project-dir
pip install urllib3 -t /path/to/project-dir
```
3. Zip the helper packages with the lambda functions

# Workflow
1. A file is uploaded to S3, if custom metadata is also specified (key value pair with key starts with `x-amz-meta-` in the header), it will be attached to the metadata field of each document.
2. Once a file is uploaded, S3 trigger the lambda function, which will index the new S3 object

# Sample request and response
## GET Request for queryableKey
```
curl https://search-velo-mfierzhwcuuhkpfrhiryttg3jq.us-east-1.es.amazonaws.com/metadata-store/images/_search\?pretty\&q\=queryableKey:"newFol_panda2.jpg"
```
## Response
```
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "hits" : {
    "total" : 1,
    "max_score" : 7.798693,
    "hits" : [
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_L-BcJg-QeBjhxETM",
        "_score" : 7.798693,
        "_source" : {
          "content_length" : 36074,
          "objectKey" : "newFol/panda2.jpg",
          "queryableKey" : "newFol_panda2.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T03:51:35+00:00",
          "metadata" : "{}"
        }
      }
    ]
  }
}
```

## GET Request for field metadata
```
curl https://search-velo-mfierzhwcuuhkpfrhiryttg3jq.us-east-1.es.amazonaws.com/metadata-store/images/_search\?pretty\&q\=metadata:devil
```
## Response
```
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "hits" : {
    "total" : 1,
    "max_score" : 1.0127578,
    "hits" : [
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_WQzEJg-QeBjhxETz",
        "_score" : 1.0127578,
        "_source" : {
          "content_length" : 94209,
          "objectKey" : "test/panda6.jpg",
          "queryableKey" : "test_panda6.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:36:34+00:00",
          "metadata" : "{\"owner\": \"devil\", \"city\": \"Boston\"}"
        }
      }
    ]
  }
}
```

## GET Request with wildcard
```
curl https://search-velo-mfierzhwcuuhkpfrhiryttg3jq.us-east-1.es.amazonaws.com/metadata-store/images/_search\?pretty\&q\=objectKey:"*panda*"
```
## Response
```
{
  "took" : 9,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "hits" : {
    "total" : 4,
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_TfOLJg-QeBjhxETr",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 62239,
          "objectKey" : "test/panda9_with_cus_metadata.jpg",
          "queryableKey" : "test_panda9_with_cus_metadata.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:24:26+00:00",
          "metadata" : "{\"gender\": \"pandas just like humans have two genders, which includes male and female\", \"age\": \"pandas usually can live around 20 years\", \"location\": \"pandas live in the forest with many other animals\"}"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_SqOWJg-QeBjhxETn",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 122558,
          "objectKey" : "test/panda4.jpg",
          "queryableKey" : "test_panda4.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:20:50+00:00",
          "metadata" : "{}"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_Sp9AJg-QeBjhxETm",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 94009,
          "objectKey" : "test/panda3.jpg",
          "queryableKey" : "test_panda3.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:20:48+00:00",
          "metadata" : "{}"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_Sp2JJg-QeBjhxETl",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 36074,
          "objectKey" : "test/panda2.jpg",
          "queryableKey" : "test_panda2.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:20:48+00:00",
          "metadata" : "{}"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_WQzEJg-QeBjhxETz",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 94209,
          "objectKey" : "test/panda6.jpg",
          "queryableKey" : "test_panda6.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:36:34+00:00",
          "metadata" : "{\"owner\": \"devil\", \"city\": \"Boston\"}"
        }
      }
    ]
  }
}
```

# Other searching requests
## GET Request "term" body
```
curl -XGET https://search-velo-mfierzhwcuuhkpfrhiryttg3jq.us-east-1.es.amazonaws.com/metadata-store/images/_search?pretty -H 'Content-Type: application/json' -d
'{
    "query" : {
        "term" : { "objectKey" : "panda" }
    }
}'
```
## Response
```
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "hits" : {
    "total" : 0,
    "max_score" : null,
    "hits" : [ ]
  }
}
```

## GET Request "prefix" body (this is used to search word with a trailing wild card) refer to [this](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-prefix-query.html)
```
curl -XGET https://search-velo-mfierzhwcuuhkpfrhiryttg3jq.us-east-1.es.amazonaws.com/metadata-store/images/_search?pretty -H 'Content-Type: application/json' -d
'{
    "query" : {
        "prefix" : { "objectKey" : "panda" }
    }
}'
```
## Response
```
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "hits" : {
    "total" : 5,
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_TfOLJg-QeBjhxETr",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 62239,
          "objectKey" : "test/panda9_with_cus_metadata.jpg",
          "queryableKey" : "test_panda9_with_cus_metadata.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:24:26+00:00",
          "metadata" : "{\"gender\": \"pandas just like humans have two genders, which includes male and female\", \"age\": \"pandas usually can live around 20 years\", \"location\": \"pandas live in the forest with many other animals\"}"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_SqOWJg-QeBjhxETn",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 122558,
          "objectKey" : "test/panda4.jpg",
          "queryableKey" : "test_panda4.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:20:50+00:00",
          "metadata" : "{}"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_Sp9AJg-QeBjhxETm",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 94009,
          "objectKey" : "test/panda3.jpg",
          "queryableKey" : "test_panda3.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:20:48+00:00",
          "metadata" : "{}"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_Sp2JJg-QeBjhxETl",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 36074,
          "objectKey" : "test/panda2.jpg",
          "queryableKey" : "test_panda2.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:20:48+00:00",
          "metadata" : "{}"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt_WQzEJg-QeBjhxETz",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 94209,
          "objectKey" : "test/panda6.jpg",
          "queryableKey" : "test_panda6.jpg",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-18T04:36:34+00:00",
          "metadata" : "{\"owner\": \"devil\", \"city\": \"Boston\"}"
        }
      }
    ]
  }
}
```

# Others
The Archive folder includes the dependency packages which you can download using `pip`
