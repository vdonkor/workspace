resource "aws_iam_role" "this" {
  assume_role_policy = data.aws_iam_policy_document.this.json
  name               = var.lambda_role_name
}
resource "aws_iam_policy" "this" {
  policy = data.aws_iam_policy_document.log.json
  name   = "${var.lambda_role_name}-policy"
}
resource "aws_iam_policy_attachment" "this" {
  name       = "${var.lambda_role_name}-attachement"
  policy_arn = aws_iam_policy.this.arn
  roles      = [aws_iam_role.this.name]
}
resource "aws_lambda_function" "this" {
  filename         = data.archive_file.this.output_path
  function_name    = var.lambda_function_name
  role             = aws_iam_role.this.arn
  handler          = "main.handler"
  memory_size      = 128
  timeout          = 60
  source_code_hash = data.archive_file.this.output_base64sha256
  runtime          = "python3.8"
  environment {
    variables = {
      SLACK_URL     = var.slack_endpoint_url
      SLACK_CHANNEL = var.slack_channel_name
    }
  }
}

resource "aws_lambda_function" "filter" {
  filename         = data.archive_file.filter.output_path
  function_name    = var.log_filter_lambda_function_name
  role             = aws_iam_role.this.arn
  handler          = "main.handler"
  memory_size      = 128
  timeout          = 60
  source_code_hash = data.archive_file.filter.output_base64sha256
  runtime          = "python3.8"
  environment {
    variables = {
      SLACK_URL     = var.slack_files_upload_endpoint_url
      SLACK_CHANNEL = var.slack_channel_name
      OAUTH_TOKEN   = var.slack_bot_user_ouath_token
    }
  }
}

resource "aws_lambda_permission" "this" {
  statement_id  = "allow_sns_function_invocation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.this.arn
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/lambda/${aws_lambda_function.this.function_name}"
  retention_in_days = 30
  tags              = var.tags
}

resource "aws_lambda_permission" "filter" {
  statement_id   = "allow_cloudwatch_log_invoke_function"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.filter.function_name
  principal      = "logs.region.amazonaws.com"
  source_arn     = "${data.aws_cloudwatch_log_group.this.arn}:"
  source_account = data.aws_caller_identity.this.account_id
}

resource "aws_cloudwatch_log_group" "filter" {
  name              = "/aws/lambda/${aws_lambda_function.filter.function_name}"
  retention_in_days = 30
  tags              = var.tags
}


