resource "aws_s3_bucket" "sensitive_data" {
  bucket = "company-financial-records-ParikshitSharma"

  tags = {
    Environment = "Production"
    DataLevel   = "Confidential"
  }
}

resource "aws_s3_bucket_acl" "sensitive_data_acl" {
  bucket = aws_s3_bucket.sensitive_data.id
  acl    = "public-read"
}
