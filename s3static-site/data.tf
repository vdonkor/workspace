#create policy document
data "aws_iam_policy_document" "public_read_policy" {
  statement {
    sid = "publicRead"
    actions = ["s3:GetObject"]
    resources = [ join("",[aws_s3_bucket.s3_website.arn,"/*"])]
    principals {
      type = "AWS"
      identifiers = ["*"]
    }
  }
}

#create policy document for redirect bucket
data "aws_iam_policy_document" "public_read_redirect_policy" {
  statement {
    sid = "publicReadRedirect"
    actions = ["s3:GetObject"]
    resources = [ join("",[aws_s3_bucket.redirect_http_https.arn,"/*"])]
    principals {
      type = "*"
      identifiers = ["*"]
    }
  }
}