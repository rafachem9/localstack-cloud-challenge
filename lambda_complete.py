import json
import boto3
import os
import traceback


endpoint_url = f'http://172.17.0.1:4566'
region = "us-east-1"
s3_filename = 'client_data.json'
bucket = 'zurich-data-lake'
table_name = 'client'


def download_file_s3(bucket_s3, s3_filename, local_filename):
    print('Downloading file to s3')
    s3 = boto3.client("s3", region_name=region, endpoint_url=endpoint_url)
    try:
        s3.download_file(Bucket=bucket_s3,
                         Key=s3_filename,
                         Filename=local_filename)
    except Exception as e:
        print(str(traceback.format_exc()))


def put_dynamo_item(dynamo_table_name, item):
    table = boto3.resource("dynamodb", region_name=region, endpoint_url=endpoint_url).Table(dynamo_table_name)
    try:
        response = table.put_item(
            Item=item
        )
        return response
    except Exception as e:
        print(e)


def lambda_handler(event, context):
    path = "/usr/tmp"
    os.chdir(path)
    download_file_s3(bucket, s3_filename, s3_filename)
    # Open the JSON file
    with open(s3_filename) as file:
        # Load the JSON data
        data = json.load(file)

    for client in data:
        print(client)
        put_dynamo_item(table_name, client)

    response = {
        'statusCode': 200,
        'body': json.dumps({'number new clients': len(data)})
    }

    return response