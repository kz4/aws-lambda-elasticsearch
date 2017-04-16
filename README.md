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
## GET Request
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
