variable "region" {
  default = "us-east-1"
  type    = string
}

variable "aws_region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "serverless-resume-upload"
}

variable "frontend_bucket_name" {
    default = "resume-frontend-kishor-2026"
    type    = string
    description = "The name of the S3 bucket to host the frontend website"
}
variable "backend_bucket_name" {
    default = "resume-backend-kishor-2026"
    type    = string
    description = "The name of the S3 bucket to store uploaded resumes"
}

variable "dynamodb_table_name" {
  default = "ResumeUploads"
  type    = string
}

variable "sns_topic_name" {
  default = "resume-upload-alerts"
  type    = string
}

variable "lambda_function_name" {
  default = "resume-upload-handler"
}
