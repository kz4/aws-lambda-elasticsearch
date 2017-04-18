# aws-lambda-elasticsearch
1. Environment is set up according to [this artile](https://aws.amazon.com/blogs/database/indexing-metadata-in-amazon-elasticsearch-service-using-aws-lambda-and-python/)
2. To get the Elasticsearch packages, run:
```
pip install requests -t /path/to/project-dir
pip install Elasticsearch -t /path/to/project-dir
pip install urllib3 -t /path/to/project-dir
```
3. Zip the helper packages with the lambda functions

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
    "max_score" : 3.873871,
    "hits" : [
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt4nUMCJg-QeBjhxEDL",
        "_score" : 3.873871,
        "_source" : {
          "content_length" : 94209,
          "objectKey" : "test/panda6.jpg",
          "queryableKey" : "test_panda6.jpg",
          "metadata" : "{\"owner\": \"devil\", \"city\": \"Boston\", \"street\": \"1 main st\"}",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-16T21:13:44+00:00"
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
    "total" : 1,
    "max_score" : 8.578434,
    "hits" : [
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt4KZupJg-QeBjhxECU",
        "_score" : 8.578434,
        "_source" : {
          "content_length" : 36074,
          "queryableKey" : "test/panda2.jpg",
          "objectKey" : "test_panda2.jpg",
          "metadata" : "{}",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-16T19:07:24+00:00"
        }
      }
    ]
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
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "hits" : {
    "total" : 694,
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt0Nj1RJg-QeBjhxD7o",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 1461,
          "objectKey" : "AWSLogs/923732660828/CloudTrail/us-east-1/2017/04/16/923732660828_CloudTrail_us-east-1_20170416T0040Z_VFFbbgdIs2088i73.json.gz",
          "queryableKey" : "AWSLogs_923732660828_CloudTrail_us-east-1_2017_04_16_923732660828_CloudTrail_us-east-1_20170416T0040Z_VFFbbgdIs2088i73.json.gz",
          "metadata" : "{}",
          "content_type" : "application/json",
          "createdDate" : "2017-04-16T00:42:43+00:00"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt0MLp3Jg-QeBjhxD7i",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 538,
          "objectKey" : "AWSLogs/923732660828/CloudTrail/us-west-2/2017/04/16/923732660828_CloudTrail_us-west-2_20170416T0030Z_6bBxVrtfsVGBVRJs.json.gz",
          "queryableKey" : "AWSLogs_923732660828_CloudTrail_us-west-2_2017_04_16_923732660828_CloudTrail_us-west-2_20170416T0030Z_6bBxVrtfsVGBVRJs.json.gz",
          "metadata" : "{}",
          "content_type" : "application/json",
          "createdDate" : "2017-04-16T00:36:41+00:00"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt0LxkIJg-QeBjhxD7h",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 1140099,
          "objectKey" : "test/IMG_5151.JPG",
          "queryableKey" : "test_IMG_5151.JPG",
          "metadata" : "{}",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-16T00:34:55+00:00"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt0NO4bJg-QeBjhxD7l",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 129500,
          "objectKey" : "test/panda1.jpg",
          "queryableKey" : "test_panda1.jpg",
          "metadata" : "{}",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-16T00:41:17+00:00"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt0LsTDJg-QeBjhxD7g",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 0,
          "objectKey" : "test/",
          "queryableKey" : "test_",
          "metadata" : "{}",
          "content_type" : "application/x-directory",
          "createdDate" : "2017-04-16T00:34:34+00:00"
        }
      }
    ]
  }
}
```

# Others
The Archive folder includes the dependency packages which you can download using `pip`
