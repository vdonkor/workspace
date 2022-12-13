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
#
variable "replicated_inventory_bucket_name" {
  type = string
  description = "name of the replicated inventory bucket"
}

variable "replication_role_name" {
  description = "name of the replication role"
  type        = string
}