provider "aws" {

  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  region                      = "us-east-1"

  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true


  endpoints {
    s3             = "http://s3.localhost.localstack.cloud:4566"
    lambda         = "http://localhost:4566"
    dynamodb        = "http://localhost:4566"
  }
}
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir   = "python/"
  output_path = "function.zip"
}


resource "aws_s3_bucket" "zurich-bucket" {
  bucket = "zurich-data-lake"
}


resource "aws_lambda_function" "lambda" {
 function_name = "localstack-lamba-url-example"
 filename         = "function.zip"
 source_code_hash = "data.archive_file.zip.output_base64sha256"
 role    = "arn:aws:iam::123456789012:role/lambda-ex"
 handler = "lamdacode.lambda_handler"
 runtime = "python3.7"
 timeout = 60
}

resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  bucket = aws_s3_bucket.zurich-bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda.arn
    events              = ["s3:ObjectCreated:*"]

  }
}


resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "client"
  billing_mode   = "PROVISIONED"
  hash_key       = "id"
  read_capacity= "30"
  write_capacity= "30"

  attribute {
    name = "id"
    type = "S"
  }

}