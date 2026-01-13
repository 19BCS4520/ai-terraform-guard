resource "aws_security_group" "web_server_sg" {
  name = "allow_all_ssh"
  description = "Allow SSH from anywhere"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    
    # VIOLATION: 0.0.0.0/0 allows access from the entire internet
    cidr_blocks = ["0.0.0.0/0"]
  }
}
