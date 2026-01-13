resource "aws_s3_bucket" "sensitive_data" {
  bucket = "parikshit-financial-records-Prigtrgkrggh5" # Bucket name must be globally unique

  tags = {
    Environment = "dev-barchart"
    DataLevel   = "Confidential"
  }
}

# VIOLATION: This separate resource controls the ACL now
resource "aws_s3_bucket_acl" "sensitive_data_acl" {
  bucket = aws_s3_bucket.sensitive_data.id
  acl    = "public-read"
}