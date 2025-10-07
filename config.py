import os
ES_HOST = os.getenv('ES_HOST', 'http://localhost:9200')
ES_INDEX = 'app_logs'
S3_BUCKET = os.getenv('S3_BUCKET', 'your-bucket-name')
S3_REGION = os.getenv('S3_REGION', 'us-east-1')
PROMETHEUS_PORT = 8000