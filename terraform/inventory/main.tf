module "inventory" {
  source = "./athena"
  athena_query_log_bucket = var.athena_query_log_bucket
  inventory_bucket_name = var.inventory_bucket_name
  athena_database_name =  var.athena_database_name
  athena_table_name = var.athena_table_name
  lambda_function_name =  var.lambda_function_name
  lambda_role_name = var.lambda_role_name
}