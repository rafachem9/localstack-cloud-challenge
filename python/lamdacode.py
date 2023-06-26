import json
from utils.constants import bucket, s3_filename, table_name
from utils.aws_utils import download_file_s3, put_dynamo_item


def lambda_handler(event, context):
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
