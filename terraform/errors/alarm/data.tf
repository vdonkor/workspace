data "aws_cloudwatch_log_group" "this" {
  name = var.cloudwatch_log_group_name
}
data "aws_caller_identity" "this" {}

data "aws_iam_policy_document" "this" {
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type = "Service"
    }
  }
}


data "aws_iam_policy_document" "log" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:*:*:*"
    ]
  }
}

data "archive_file" "this" {
  type        = "zip"
  output_path = "${path.module}/send-slack.zip"
  source_file = "${path.module}/src/slack/main.py"
}
data "archive_file" "filter" {
  type        = "zip"
  output_path = "${path.module}/log-filter.zip"
  source_file = "${path.module}/src/filter/main.py"
}
