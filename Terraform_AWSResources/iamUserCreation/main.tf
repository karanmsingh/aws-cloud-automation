// AWS credentials can be saved in C:\Users\Karan\.aws\credentials. These will be used to interact with the account

provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_user" "admin-user" {
	name = "lucy"
	tags = {
	Description = "Automated with Terraform."
	}
}


resource "aws_iam_policy" "adminUser" {
	name = "AdminUsers"
	policy = <<EOF
	{
  	"Version": "2012-10-17",
  	"Statement": [
    		{
      		"Effect": "Allow",
		"Action": "*",
		"Resource": "*"
		}
	     ]
	}
EOF
}

resource "aws_iam_user_policy_attachment" "lucy-attachment" {
  user       = aws_iam_user.admin-user.name
  policy_arn = aws_iam_policy.adminUser.arn
}
