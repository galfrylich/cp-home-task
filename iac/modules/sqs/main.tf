resource "aws_sqs_queue" "this" {
  name                       = var.name
  visibility_timeout_seconds = 30
  message_retention_seconds  = 86400  # 1 day

  tags = {
    Name = var.name
  }
}