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
  s3_use_path_style           = true

  # Direct all AWS API endpoints to local MiniStack
  endpoints {
    cloudwatch = "http://localhost:4566"
    dynamodb   = "http://localhost:4566"
    s3         = "http://localhost:4566"
    sns        = "http://localhost:4566"
    sqs        = "http://localhost:4566"
  }
}

# -------------------------------------------------------------
# 1. Alert Notification (SNS)
# -------------------------------------------------------------
resource "aws_sns_topic" "sre_alerts" {
  name = "sre-alerts-topic"
}

# -------------------------------------------------------------
# 2. Dead Letter & Incident Queue (SQS)
# -------------------------------------------------------------
resource "aws_sqs_queue" "sre_dlq" {
  name = "sre-dlq"
}

# Subscribe the SQS queue to the SNS topic
resource "aws_sns_topic_subscription" "alerts_to_sqs" {
  topic_arn = aws_sns_topic.sre_alerts.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.sre_dlq.arn
}

# -------------------------------------------------------------
# 3. Observability & Alarm (CloudWatch)
# -------------------------------------------------------------
resource "aws_cloudwatch_metric_alarm" "high_error_rate" {
  alarm_name          = "high-error-rate-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "HTTPCode_Target_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Triggers when target 5xx errors exceed threshold."

  # Route alarm breach directly to the SNS alert topic
  alarm_actions = [aws_sns_topic.sre_alerts.arn]
}

# -------------------------------------------------------------
# 4. Storage & Incident State (S3 & DynamoDB)
# -------------------------------------------------------------
resource "aws_s3_bucket" "audit_logs" {
  bucket = "sre-audit-logs-local"
}

resource "aws_dynamodb_table" "incidents" {
  name         = "incidents-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "IncidentId"

  attribute {
    name = "IncidentId"
    type = "S"
  }
}

# -------------------------------------------------------------
# Terraform Outputs
# -------------------------------------------------------------
output "sns_topic_arn" {
  value = aws_sns_topic.sre_alerts.arn
}

output "sqs_queue_url" {
  value = aws_sqs_queue.sre_dlq.id
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.incidents.name
}