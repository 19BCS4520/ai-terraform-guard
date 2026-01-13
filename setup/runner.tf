provider "aws" {
  region = "us-east-1"
}

# 1. Security Group: Outbound only (Secure)
resource "aws_security_group" "runner_sg" {
  name        = "ai-runner-sg"
  description = "Security group for GitHub Runner"

  # Allow SSH from ANYWHERE (For your initial setup only)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 2. The Instance (The Worker)
resource "aws_instance" "runner" {
  ami           = "ami-0ecb62995f68bb549" # Ubuntu 22.04 (us-east-1)
  instance_type = "t3.medium"             # Allowed Type
  key_name      = "my-key-pair"           # <--- CHANGE THIS to your Key Pair name

  vpc_security_group_ids = [aws_security_group.runner_sg.id]
  
  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  # Startup Script: Installs Tools automatically
  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y jq python3-pip unzip curl
    
    # Install Terrascan (The Scanner)
    curl -L "$(curl -s https://api.github.com/repos/tenable/terrascan/releases/latest | grep -o -E "https://.+?_Linux_x86_64.tar.gz")" > terrascan.tar.gz
    tar -xf terrascan.tar.gz terrascan && install terrascan /usr/local/bin
    
    # Install Python Requests (For talking to Gemini)
    pip3 install requests
    
    # Create Runner Directory
    mkdir /actions-runner && cd /actions-runner
  EOF

  tags = { Name = "AI-Runner" }
}

output "runner_ip" {
  value = aws_instance.runner.public_ip
}