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

data "aws_iam_policy_document" "s3" {
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:GetObjectVersion",
    ]
    resources = ["arn:aws:s3:::${aws_s3_bucket.this.bucket}/*"]
  }
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.this.bucket}"
    ]
  }
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
  output_path = "${path.module}/write-bucket.zip"
  source_file = "${path.module}/src/main.py"
}
