import boto3
from utils.constants import region, endpoint_url


def get_key_dynamo(dynamotable, key):
    try:
        dynamo_client = boto3.client("dynamodb", region_name=region, endpoint_url=endpoint_url)
        response = dynamo_client.get_item(
            TableName=dynamotable,
            Key=key
        )
        return response['Item']
    except Exception as e:
        print(e)


def put_dynamo_item(dynamo_table_name, item):
    table = boto3.resource("dynamodb", region_name=region, endpoint_url=endpoint_url).Table(dynamo_table_name)
    try:
        response = table.put_item(
            Item=item
        )
        return response
    except Exception as e:
        print(e)


def upload_file_s3(bucket, s3_filename, local_file):
    print('Uploading file to s3')
    s3 = boto3.client("s3", region_name=region, endpoint_url=endpoint_url)
    s3.upload_file(local_file, bucket, s3_filename)


def download_file_s3(bucket_s3, s3_filename, local_filename):
    print('Downloading file to s3')
    s3 = boto3.client("s3", region_name=region, endpoint_url=endpoint_url)
    s3.download_file(Bucket=bucket_s3,
                     Key=s3_filename,
                     Filename=local_filename)

