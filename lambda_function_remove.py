from __future__ import print_function
from pprint import pprint
import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
import urllib
import re

index_name = 'metadata-store'
index_type = 'images'
endpoint = 'search-velo-mfierzhwcuuhkpfrhiryttg3jq.us-east-1.es.amazonaws.com'

print('Loading function')

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

def clearMetaData(esClient,key):
    try:
        print("queryableKey: " + key)
        # retval = esClient.search(index=index_name, doc_type=index_type, q='objectKey:' + key, fielddata_fields='_id')
        retval = esClient.search(index=index_name, doc_type=index_type, q='queryableKey:' + key)
        print("retval: {}".format(retval))
        total = retval['hits']['total']
        count = 0
        # while (count < total):  
        #     docId = retval['hits']['hits'][count]['_id']
        #     print("Deleting: " + docId)
        #     removeDocElement(esClient,docId)
        #     count = count + 1

        # We want to delete the first one because we can get multiple results with similar structure,
        # e.g. curl https://search-velo-mfierzhwcuuhkpfrhiryttg3jq.us-east-1.es.amazonaws.com/metadata-store/all/_search\?pretty\&q\=queryableKey:"newFol_panda4.jpg"
        # returns: newFol_panda4.jpg and newFol_panda6.jpg
        docId = retval['hits']['hits'][count]['_id']
        print("Deleting: " + docId)
        removeDocElement(esClient,docId)

        return 1        
    except Exception as E:
        print("Removing metadata failed")
        print("Error: ",E)
        exit(5)


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

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    # queryableKey = key.replace("/", "_")
    queryableKey = re.sub(r'\W+', '', key)
    try:
        clearMetaData(esClient,queryableKey)
        return 'Removed metadata for ' + key
    except Exception as e:
        print(e)
        print('Error removing object metadata from ElasticSearch Domain.')
        raise e
