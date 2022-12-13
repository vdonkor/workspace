variable "region" {
  default = "us-east-1"
  description = "aws region"
  type = string
}
variable "lambda_role_name" {
  description = "name of the lambda role"
  type        = string
}

variable "lambda_function_name" {
  type = string
  description = "name of this lambda function"
}
variable "inventory_bucket_name" {
  type = string
  description = "name of the inventory bucket"
}
variable "athena_query_log_bucket" {
  type = string
  description = "athena query log bucket name"
}
variable "athena_database_name" {
  type = string
  description = "name of the athena database"
}
variable "athena_table_name" {
  type = string
  description = "name of the athena table"
}
variable "stack_name" {
  type = string
  description = "name of this stack"
  default = "echs"
}