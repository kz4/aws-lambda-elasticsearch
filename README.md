# aws-lambda-elasticsearch
1. Environment is set up according to [this artile](https://aws.amazon.com/blogs/database/indexing-metadata-in-amazon-elasticsearch-service-using-aws-lambda-and-python/)
2. To get the Elasticsearch packages, run:
```
pip install requests -t /path/to/project-dir
pip install Elasticsearch -t /path/to/project-dir
pip install urllib3 -t /path/to/project-dir
```
3. Zip the helper packages with the lambda functions
