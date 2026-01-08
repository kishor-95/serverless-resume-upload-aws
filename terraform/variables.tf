variable "region" {
  default = "us-east-1"
  type = string
}

variable "aws_region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "serverless-resume-upload"
}

variable "frontend_bucket_name" {}
variable "backend_bucket_name" {}

variable "dynamodb_table_name" {
    default = "ResumeUploads"
    type = string
}

variable "sns_topic_name" {
    default = "resume-upload-alerts"
    type = string
}

variable "lambda_function_name" {
    default = "resume-upload-handler"
}
