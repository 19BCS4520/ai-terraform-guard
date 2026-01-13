resource "aws_db_instance" "payments_db" {
  allocated_storage    = 10
  engine               = "mysql"
  instance_class       = "db.t3.micro"
  db_name              = "payments_prod"
  username             = "admin"
  
  # VIOLATION 1: Hardcoded weak password
  password             = "Password123!" 
  
  # VIOLATION 2: The database is open to the entire internet
  publicly_accessible  = true 
  
  # VIOLATION 3: Data is not encrypted at rest
  storage_encrypted    = false 
  
  skip_final_snapshot  = true
}
