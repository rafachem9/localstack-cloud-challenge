from utils.utils import log_handler
endpoint_url = f'http://172.17.0.1:4566'
region = "us-east-1"
s3_filename = 'client_data.json'
bucket = 'zurich-data-lake'
table_name = 'client'

logger = log_handler('zurich-logs')