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
## GET Request without body
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
          "metadata" : "{\"owner\": \"devil\", \"city\": \"Boston\", \"street\": \"1 main st\"}",
          "content_type" : "image/jpeg",
          "createdDate" : "2017-04-16T21:13:44+00:00"
        }
      }
    ]
  }
}
```
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
          "objectKey" : "test/panda2.jpg",
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
          "metadata" : "{}",
          "content_type" : "application/json",
          "createdDate" : "2017-04-16T00:36:41+00:00"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt0MU2lJg-QeBjhxD7j",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 4692,
          "objectKey" : "AWSLogs/923732660828/CloudTrail/us-east-1/2017/04/16/923732660828_CloudTrail_us-east-1_20170416T0035Z_TCDSQEreexAaz1xy.json.gz",
          "metadata" : "{}",
          "content_type" : "application/json",
          "createdDate" : "2017-04-16T00:37:20+00:00"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt0MZUAJg-QeBjhxD7k",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 1458,
          "objectKey" : "AWSLogs/923732660828/CloudTrail/us-east-1/2017/04/16/923732660828_CloudTrail_us-east-1_20170416T0035Z_XCKMJMJAnllHu8ly.json.gz",
          "metadata" : "{}",
          "content_type" : "application/json",
          "createdDate" : "2017-04-16T00:37:38+00:00"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt0NfCIJg-QeBjhxD7m",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 791,
          "objectKey" : "AWSLogs/923732660828/CloudTrail/us-east-1/2017/04/16/923732660828_CloudTrail_us-east-1_20170416T0040Z_1UCYpvlnuj66rO0K.json.gz",
          "metadata" : "{}",
          "content_type" : "application/json",
          "createdDate" : "2017-04-16T00:42:23+00:00"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt0NideJg-QeBjhxD7n",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 685,
          "objectKey" : "AWSLogs/923732660828/CloudTrail/us-east-1/2017/04/16/923732660828_CloudTrail_us-east-1_20170416T0040Z_JWyCacnRi2ovRkmp.json.gz",
          "metadata" : "{}",
          "content_type" : "application/json",
          "createdDate" : "2017-04-16T00:42:38+00:00"
        }
      },
      {
        "_index" : "metadata-store",
        "_type" : "images",
        "_id" : "AVt0LqGuJg-QeBjhxD7f",
        "_score" : 1.0,
        "_source" : {
          "content_length" : 383,
          "objectKey" : "undefined2017-04-16-00-31-41-953311A33B3F8FFD",
          "metadata" : "{}",
          "content_type" : "text/plain",
          "createdDate" : "2017-04-16T00:31:42+00:00"
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
          "metadata" : "{}",
          "content_type" : "application/x-directory",
          "createdDate" : "2017-04-16T00:34:34+00:00"
        }
      }
    ]
  }
}
```

