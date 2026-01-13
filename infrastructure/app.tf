resource "aws_instance" "test_server" {
  ami           = "ami-0ecb62995f68bb549"
  instance_type = "t3.micro"
  
  # 🚨 VIOLATION: Using the dangerous Lab Role
  iam_instance_profile = "EC2LabRole" 
  
  tags = {
    Name = "Trojan-Horse-Instance"
  }
}# Triggering AI Security Review
