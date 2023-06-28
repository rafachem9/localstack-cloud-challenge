# NUWE-Zurich-Cloud-Hackathon
This repository contains all the files needed to start the online phase of the NUWE x Zurich Cloud Challenge.
https://nuwe.io/dev/competitions/zurich-cloud-hackathon/online-preselection-cloud-challenge

# Localstack examples:
https://github.com/localstack/localstack-terraform-samples/blob/master/s3-lambda-sqs-notification/main.tf

Pendiente de leer:
https://levelup.gitconnected.com/how-to-test-s3-with-terraform-using-localstack-585d2366fa13

## Schema architecture:
![Alt text](/tecnical-documentation/Zurich-cloud-challenge.png "Optional title")

## Local execution:
### Localstack
- To test this project, it is necessary to activate the localstack server in order to emulate AWS services:
`docker-compose up`
- Comments: We attempted to execute the project by installing localstack using pip, but encountered an error in the communication between the created containers. In the docker-compose.yaml file, we have added an environment variable:
`DOCKER_BRIDGE_IP=172.17.0.1`

### Terraforms 
- To deploy the services, we execute the following commands:
  - `terraform init`
  - `terraform plan`
  - `terraform apply`

### Lambda activation
- In order to activate the lambda function, you can utilize the following command to upload a file to S3 (do not change destination file name):
`aws s3 cp data/client_data.json s3://zurich-data-lake/client_data.json --endpoint-url http://localhost:4566`