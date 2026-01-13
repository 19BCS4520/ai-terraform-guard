resource "aws_s3_bucket" "financial_records" {
  bucket = "company-financial-data-2024"
  
  # VIOLATION: Public Access
  acl    = "public-read"
  
  tags = {
    DataLevel = "Confidential"
  }
}
