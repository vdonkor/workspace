resource "aws_sns_topic" "this" {
  name = var.sns_topic_name
}
resource "aws_sns_topic_subscription" "this" {
  endpoint               = aws_lambda_function.this.arn
  protocol               = "lambda"
  endpoint_auto_confirms = true
  topic_arn              = aws_sns_topic.this.arn
}