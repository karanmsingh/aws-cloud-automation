terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    ec2 = "http://localhost:4566"
  }
}

# 1. Dummy AMI / Subnet
resource "aws_vpc" "dev_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "dev_subnet" {
  vpc_id     = aws_vpc.dev_vpc.id
  cidr_block = "10.0.1.0/24"
}

# 2. Target EC2 Instance matching script tags
resource "aws_instance" "dev_server_1" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.dev_subnet.id

  tags = {
    Environment = "Dev"
    Name        = "dev-worker-1"
  }
}

resource "aws_instance" "dev_server_2" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.dev_subnet.id

  tags = {
    Environment = "Dev"
    Name        = "dev-worker-2"
  }
}

# 3. Non-matching instance (should be ignored by script)
resource "aws_instance" "prod_server" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.dev_subnet.id

  tags = {
    Environment = "Prod"
    Name        = "prod-worker-1"
  }
}
