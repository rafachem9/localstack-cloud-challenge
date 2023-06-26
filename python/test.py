import boto3
from botocore.client import Config
from utils.aws_utils import download_file_s3, upload_file_s3, put_dynamo_item, get_key_dynamo
import json


table_name = 'employee'  # Cambia el nombre de la tabla
item = {
    'id': "1",  # Ejemplo de atributo 'id' de tipo String
    'name': {'S': 'Ejemplo2'},  # Ejemplo de atributo 'name' de tipo String
    'age': {'N': '25'},  # Ejemplo de atributo 'age' de tipo Number
}
key = {'id': {"S": '1'}}
bucket = 'my-bucket'
s3_filename = 'client_data.json'
# put_dynamo_item(table_name, item)

# download_file_s3(bucket, s3_filename, s3_filename)
#
# # Open the JSON file
# with open(s3_filename) as file:
#     # Load the JSON data
#     data = json.load(file)


# for client in data:
#     print(client)
# #     put_dynamo_item(table_name, client)
key = {'id': {"S": '498-22-7330'}}

response = get_key_dynamo(table_name, key)
print(response)
#
# with open(s3_filename) as file:
#     # Load the JSON data
#     data = json.load(file)
#
# response = {
#     'statusCode': 200,
#     'body': json.dumps({'number new clients': len(data)})
# }
#
# print(response)