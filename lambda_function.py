from __future__ import print_function
from pprint import pprint
import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection

import urllib
import json
import re

s3 = boto3.client('s3')
index_name = 'metadata-store'
index_type = 'images'
endpoint = 'search-velo-mfierzhwcuuhkpfrhiryttg3jq.us-east-1.es.amazonaws.com'

print('Loading function')

indexDoc = {
    "dataRecord" : {
        "properties" : {
          "createdDate" : {
            "type" : "date",
            "format" : "dateOptionalTime"
          },
          "objectKey" : {
            "type" : "string"
          },
          "queryableKey" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "content_type" : {
            "type" : "string"
          },
          "content_length" : {
            "type" : "long"
          },
          "metadata" : {
            "type" : "string"
          }
        }
      },
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
      }
    }


def connectES(esEndPoint):
    print ('Connecting to the ES Endpoint {0}'.format(esEndPoint))
    try:
        esClient = Elasticsearch(
            hosts=[{'host': esEndPoint, 'port': 443}],
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection)
        return esClient
    except Exception as E:
        print("Unable to connect to {0}".format(esEndPoint))
        print(E)
        exit(3)

def createIndex(esClient):
    try:
        res = esClient.indices.exists(index_name)
        if res is False:
            print("Creating index: " + index_name)
            esClient.indices.create(index_name, body=indexDoc)
            return 1
    except Exception as E:
            print("Unable to Create Index {0}".format(index_name))
            print(E)
            exit(4)

def indexDocElement(esClient,key,response):
    # queryableKey = key.replace("/", "_")
    queryableKey = re.sub(r'\W+', '', key)
    try:
        clearMetaData(esClient,queryableKey)
        body ='''
        {
          "query" : {
            "constant_score" : {
                "filter" : {
                    "term" : {
                        "queryableKey" :"''' + queryableKey + '''"
                    }
                }
            }
        }
        }'''
        print("body: {}".format(body))
        retval2 = esClient.search(index=index_name, doc_type=index_type, body=body)
        print("retval2: {}".format(retval2))
    except Exception as e:
        print(e)
        print('Error removing object metadata from ElasticSearch Domain or file does not exist.')

    try:
        indexObjectKey = key
        indexcreatedDate = response['LastModified']
        indexcontent_length = response['ContentLength']
        indexcontent_type = response['ContentType']
        indexmetadata = json.dumps(response['Metadata'])
        retval = esClient.index(index=index_name, doc_type=index_type, body={
                'createdDate': indexcreatedDate,
                'objectKey': indexObjectKey,
                'queryableKey': queryableKey,
                'content_type': indexcontent_type,
                'content_length': indexcontent_length,
                'metadata': indexmetadata
        })
        print("indexed: " + indexObjectKey)
    except Exception as E:
        print("Document not indexed")
        print("Error: ",E)
        exit(6)
      
def clearMetaData(esClient,key):
    try:
        print("queryableKey: " + key)
        # retval = esClient.search(index=index_name, doc_type=index_type, q='objectKey:' + key, fielddata_fields='_id')
        retval = esClient.search(index=index_name, doc_type=index_type, q='queryableKey:' + key)
        print("retval: {}".format(retval))
        total = retval['hits']['total']
        count = 0
        if total > 0:
            docId = retval['hits']['hits'][count]['_id']
            print("Deleting: " + docId)
            removeDocElement(esClient,docId)
            return 1
    except Exception as E:
        print("Removing metadata failed")
        print("Error: ",E)
        # exit(5)

def removeDocElement(esClient,docId):
    try:
        retval = esClient.delete(index=index_name, doc_type=index_type, id=docId)
        print("Deleted: " + docId)
        return 1
    except Exception as E:
        print("DocId delete command failed at ElasticSearch.")
        print("Error: ",E)
        exit(5)

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    esClient = connectES(endpoint)
    createIndex(esClient)

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        indexDocElement(esClient,key,response)
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
