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
#  source_dir   = "python/"
  source_file = "lambda_complete.py"
  output_path = "function.zip"
}


resource "aws_s3_bucket" "test-bucket" {
  bucket = "my-bucket"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "my-s3-read-policy" {
  name   = "lambda-s3-policy"
  role   = "iam_for_lambda"
  policy = data.aws_iam_policy_document.s3_read_permissions.json
}

data "aws_iam_policy_document" "s3_read_permissions" {
  statement {
    effect = "Allow"
    actions = [
              "s3:PutObject",
              "s3:PutObjectAcl",
              "s3:GetObject",
              "s3:GetObjectAcl",
              "s3:HeadObject",
              "s3:DeleteObject",
              "s3:ListBucketMultipartUploads",
              "s3:ListBucket",
              "s3:ListMultipartUploadParts",
    ]
    resources = ["arn:aws:s3:::my-bucket",
                "arn:aws:s3:::my-bucket/*",
    ]
  }
}


resource "aws_lambda_function" "lambda" {
 function_name = "localstack-lamba-url-example"
 filename         = "function.zip"
 source_code_hash = "data.archive_file.zip.output_base64sha256"
 role    = aws_iam_role.iam_for_lambda.arn
 handler = "lambda_complete.lambda_handler"
 runtime = "python3.7"
 timeout = 60
}
# https://kuros.in/aws/terraform/fix-lambda-function-url-on-localstack/
resource "aws_lambda_function_url" "function_url" {

  function_name = aws_lambda_function.lambda.function_name
  authorization_type = "NONE"

}
resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  bucket = aws_s3_bucket.test-bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda.arn
    events              = ["s3:ObjectCreated:*",
                           "s3:ObjectRemoved:*"]

  }
}


resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "employee"
  billing_mode   = "PROVISIONED"
  hash_key       = "id"
  read_capacity= "30"
  write_capacity= "30"

  attribute {
    name = "id"
    type = "S"
  }

}

output "url" {
  value = aws_lambda_function_url.function_url
}