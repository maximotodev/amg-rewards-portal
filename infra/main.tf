# 1. Create a VPC for the AMG Rewards Portal
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "${var.project_name}-vpc" }
}

# 2. Create a Private Subnet for the Database
resource "aws_db_subnet_group" "default" {
  name       = "${var.project_name}-db-subnet"
  subnet_ids = [aws_subnet.private_1.id, aws_subnet.private_2.id]
}

# 3. Managed MySQL (RDS) - This replaces your local Docker MySQL
resource "aws_db_instance" "mysql" {
  identifier           = "${var.project_name}-db"
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.4"
  instance_class       = "db.t3.micro" # Cost-effective for demo
  db_name              = "amg_rewards"
  username             = "amg"
  password             = var.db_password
  db_subnet_group_name = aws_db_subnet_group.default.name
  skip_final_snapshot  = true
  multi_az             = false # Set to true for real production high-availability
}