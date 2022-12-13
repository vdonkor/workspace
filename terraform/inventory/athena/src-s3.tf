#create s3 bucket for source
resource "aws_s3_bucket" "src" {
  bucket = "${var.stack_name}-${var.inventory_bucket_name}"
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
  replication_configuration {
    role = aws_iam_role.src_replication_role.arn
    rules {
      status = "Enabled"
      destination {
        bucket = aws_s3_bucket.dest.arn
        storage_class = "STANDARD"
        access_control_translation {
          owner = "Destination"
        }
        account_id = data.aws_caller_identity.dest.account_id
      }
    }
  }
}

# set bucket acl
resource "aws_s3_bucket_acl" "this" {
  bucket = aws_s3_bucket.src.id
  acl    = "private"
}

# set object ownership
resource "aws_s3_bucket_ownership_controls" "src" {
  bucket = aws_s3_bucket.src.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

#assume policy document
data "aws_iam_policy_document" "src_sts" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }
  }
}

#replication policy for the repliation role
data "aws_iam_policy_document" "src_replication_policy" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetReplicationConfiguration",
      "s3:GetBucketAcl",
      "s3:GetBucketPolicy",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.src.arn,
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObjectVersionForReplication",
      "s3:GetObjectVersionAcl",
      "s3:GetObjectVersionTagging",
      "s3:GetObjectRetention",
      "s3:GetObjectLegalHold"
    ]
    resources = [
      "${aws_s3_bucket.src.arn}/*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:ReplicateObject",
      "s3:ReplicateDelete",
      "s3:ReplicateTags",
      "s3:ObjectOwnerOverrideToBucketOwner"
    ]
    resources = [
      "${aws_s3_bucket.dest.arn}/*",
    ]
  }
}

resource "aws_iam_role" "src_replication_role" {
  name               =  "${var.stack_name}-${var.replication_role_name}"
  assume_role_policy =  data.aws_iam_policy_document.src_sts.json
}

resource "aws_iam_policy" "source_replication" {
  name     = "${var.stack_name}-replication-policy"
  policy   = data.aws_iam_policy_document.src_replication_policy.json
}

resource "aws_iam_role_policy_attachment" "src_policy_attachment" {
  role       =  aws_iam_role.src_replication_role.name
  policy_arn =  aws_iam_policy.source_replication.arn
}
