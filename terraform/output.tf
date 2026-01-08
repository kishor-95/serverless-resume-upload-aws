output "frontend_bucket" {
  value = aws_s3_bucket.frontend.bucket
}
output "frontend_website_url" {
  value = aws_s3_bucket_website_configuration.frontend.website_endpoint
}

output "dynamodb_table" {
  value = aws_dynamodb_table.resume_uploads.name
}

output "sns_topic_arn" {
  value = aws_sns_topic.alerts.arn
}
output "backend_bucket" {
  value = aws_s3_bucket.resume_storage.bucket
}
output "lambda_function_name" {
  value = aws_lambda_function.upload.function_name
}
