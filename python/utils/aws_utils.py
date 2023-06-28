import boto3
from utils.constants import region, endpoint_url
import traceback
from utils.constants import logger
from utils.utils import flush_handlers


def get_key_dynamo(dynamotable, key):
    try:
        dynamo_client = boto3.client("dynamodb", region_name=region, endpoint_url=endpoint_url)
        response = dynamo_client.get_item(
            TableName=dynamotable,
            Key=key
        )
        return response['Item']
    except Exception:
        logger.error(str(traceback.format_exc()))
        flush_handlers(logger)


def download_file_s3(bucket_s3, s3_filename, local_filename):
    logger.info('Downloading file to s3')
    flush_handlers(logger)
    s3 = boto3.client("s3", region_name=region, endpoint_url=endpoint_url)
    try:
        s3.download_file(Bucket=bucket_s3,
                         Key=s3_filename,
                         Filename=local_filename)
    except Exception:
        logger.error(str(traceback.format_exc()))


def upload_file_s3(bucket, s3_filename, local_file):
    logger.info('Uploading file to s3')
    flush_handlers(logger)
    s3 = boto3.client("s3", region_name=region, endpoint_url=endpoint_url)
    s3.upload_file(local_file, bucket, s3_filename)


def put_dynamo_item(dynamo_table_name, item):
    logger.info(f'Adding item to {dynamo_table_name}')
    flush_handlers(logger)
    table = boto3.resource("dynamodb", region_name=region, endpoint_url=endpoint_url).Table(dynamo_table_name)
    try:
        response = table.put_item(
            Item=item
        )
        return response
    except Exception:
        logger.error(str(traceback.format_exc()))
        flush_handlers(logger)


