# Providing the access to the AWS S3 bucket.
 
resource "aws_s3_bucket_public_access_block" "publicaccess" {
  bucket = aws_s3_bucket.demobucket.id
  block_public_acls       = false
  block_public_policy     = false
}
 
# Creating the encryption key which will encrypt the bucket objects
 
resource "aws_kms_key" "mykey" {
  deletion_window_in_days = "20"
}
 
# Creating the AWS S3 bucket.
 
resource "aws_s3_bucket" "demobucket" {
 
  bucket          = var.bucket
  force_destroy   = var.force_destroy
 
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = aws_kms_key.mykey.arn
        sse_algorithm     = "aws:kms"
      }
    }
  }
  versioning {
    enabled          = true
  }
  lifecycle_rule {
    prefix  = "log/"
    enabled = true
    expiration {
      date = var.date
    }
  }
}