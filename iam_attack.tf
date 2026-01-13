resource "aws_iam_role" "EC2LabRole" {
  name = "EC2LabRole"

  # VIOLATION: This role allows an EC2 instance to become an Admin
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "admin_attach" {
  role       = aws_iam_role.EC2LabRole.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}
