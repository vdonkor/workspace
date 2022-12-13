#create destination bucket
resource "aws_s3_bucket" "dest" {
  provider = "aws.dest"
  bucket = var.replicated_inventory_bucket_name
  acl    = "private"
  versioning {
    enabled = true
  }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
#set ownership of the bucket
resource "aws_s3_bucket_ownership_controls" "dest" {
  provider = "aws.dest"
  bucket = aws_s3_bucket.dest.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}
#block public access
resource "aws_s3_bucket_public_access_block" "dest" {
  provider = "aws.dest"
  bucket                  = aws_s3_bucket.dest.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
#apply bucket policy
resource "aws_s3_bucket_policy" "dest" {
  provider = "aws.dest"
  bucket   = aws_s3_bucket.dest.id
  policy   = data.aws_iam_policy_document.dest_bucket_policy
}

#set bucket policy
data "aws_iam_policy_document" "dest_bucket_policy" {
  provider = "aws.dest"
  statement {
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [
        aws_iam_role.src_replication_role.arn,
      ]
    }
    actions = [
      "s3:ReplicateObject",
      "s3:ReplicateDelete"
    ]
    resources = ["${aws_s3_bucket.dest.arn}/*"]
  }
  statement {
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [
        aws_iam_role.src_replication_role.arn,
      ]
    }
    actions = [
      "s3:List*",
      "s3:GetBucketVersioning",
      "s3:PutBucketVersioning"
    ]
    resources = [aws_s3_bucket.dest.arn]
  }
  statement {
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [
        aws_iam_role.src_replication_role.arn,
      ]
    }
    actions = [
      "s3:ReplicateObject",
      "s3:ReplicateDelete",
      "s3:ReplicateTags",
      "s3:PutObject",
      "s3:ObjectOwnerOverrideToBucketOwner",
      "s3:GetObjectVersionTagging",
      "s3:GetObjectVersionForReplication",
    ]
    resources = ["${aws_s3_bucket.dest.arn}/*"]
  }
}

