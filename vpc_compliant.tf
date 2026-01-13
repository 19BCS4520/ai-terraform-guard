resource "aws_vpc" "main_secure" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name        = "main-secure-vpc"
    Environment = "Production"
  }
}

# GOOD PRACTICE: Enabling Flow Logs for auditing
resource "aws_flow_log" "main_audit" {
  iam_role_arn    = "arn:aws:iam::123456789012:role/flow-log-role"
  log_destination = "arn:aws:logs:us-east-1:123456789012:log-group:vpc-flow-logs"
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.main_secure.id
}
