provider "aws" {

	region = "us-east-1"

}


resource "aws_s3_bucket" "example" {

	bucket = "kaststb-terraform"
	tags = {
		Description = "Created with Terraform."
	}

}