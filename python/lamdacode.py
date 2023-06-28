import os
import json
import logging
from utils.constants import bucket, s3_filename, table_name, logger
from utils.aws_utils import download_file_s3, put_dynamo_item
from utils.utils import flush_handlers


def lambda_handler(event, context):
    try:
        logger.info('Starting Updating Client Process')
        flush_handlers(logger)
        path = "/usr/tmp"
        os.chdir(path)
        download_file_s3(bucket, s3_filename, s3_filename)
        # Open the JSON file
        with open(s3_filename) as file:
            # Load the JSON data
            data = json.load(file)

        for client in data:
            logging.info('Updating cliente: ', client)
            put_dynamo_item(table_name, client)

        logger.info(f'number of new clients {len(data)}')
        logger.info('Finishing Updating Client Process')
        flush_handlers(logger)
        response = {
            'statusCode': 200,
            'body': json.dumps({'number new clients': len(data)})
        }
        return response

    except Exception as e:
        logger.error(str(e))
        flush_handlers(logger)
        return {
            'statusCode': 500,
            'body': json.dumps({'Internal Error': str(e)})
        }

lambda_handler('test', 'test')