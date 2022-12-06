resource "aws_iam_role" "this" {
  assume_role_policy = data.aws_iam_policy_document.this.json
  name               =  "${var.stack_name}-${var.lambda_role_name}"
}
resource "aws_iam_policy" "this" {
  policy = data.aws_iam_policy_document.s3.json
  name   = "${var.stack_name}-${var.lambda_role_name}-policy"
}
resource "aws_iam_policy_attachment" "this" {
  name       = "${var.stack_name}-${var.lambda_role_name}-attachement"
  policy_arn = aws_iam_policy.this.arn
  roles      = [aws_iam_role.this.name]
}
resource "aws_lambda_function" "this" {
  filename         = data.archive_file.this.output_path
  function_name    = "${var.stack_name}-${var.lambda_function_name}"
  role             = aws_iam_role.this.arn
  handler          = "main.handler"
  memory_size      = 128
  timeout          = 60
  source_code_hash = data.archive_file.this.output_base64sha256
  runtime          = "python3.8"
  environment {
    variables = {
      S3_BUCKET     = aws_s3_bucket.this.bucket
      ATHENA_QUERY_LOG_BUCKET = var.athena_query_log_bucket
      ATHENA_DATABASE_NAME = var.athena_database_name
      ATHENA_TABLE_NAME = var.athena_table_name
  }
}

}

resource "aws_cloudwatch_event_rule" "this" {
  name = "${var.stack_name}-data-warehouse-inventory-every-7am"
  description = "run data warehouse inventory  7am"
  schedule_expression = "cron(0 7 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "this" {
  rule = aws_cloudwatch_event_rule.this.name
  target_id = "${var.stack_name}-data-warehouse-inventory"
  arn = aws_lambda_function.this.arn
}

resource "aws_lambda_permission" "cloudwatch_invoke_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.this.arn
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/lambda/${aws_lambda_function.this.function_name}"
  retention_in_days = 30
}



