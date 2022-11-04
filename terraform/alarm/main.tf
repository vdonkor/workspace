#create metric filter
resource "aws_cloudwatch_log_metric_filter" "this" {
  name            = var.metric_filter_name
  pattern         = var.metric_filter_pattern
  log_group_name  = data.aws_cloudwatch_log_group.this.name
  metric_transformation {
    name          = var.metric_transformation_name
    namespace     = var.metric_transformation_namespace
    value         = var.metric_transformation_value
    default_value = var.metric_transformation_default_value
    unit          = ""
  }
}

#create alarm
resource "aws_cloudwatch_metric_alarm" "this" {
  actions_enabled           =  var.actions_enabled
  alarm_name                =  var.alarm_name
  comparison_operator       =  var.comparison_operator
  datapoints_to_alarm       =  var.datapoints_to_alarm
  evaluation_periods        = "5"
  metric_name               = aws_cloudwatch_log_metric_filter.this.name
  namespace                 = var.metric_transformation_namespace
  period                    = var.period
  statistic                 = var.statistic
  threshold                 = var.threshold
  alarm_description         = var.alarm_description
  treat_missing_data        = var.treat_missing_data
  alarm_actions             = [aws_sns_topic.this.arn]
}

#create subscription filter
resource "aws_cloudwatch_log_subscription_filter" "this" {
  name            =  var.cloudwatch_log_subscription_filter_name
  role_arn        = aws_iam_role.this.arn
  log_group_name  = data.aws_cloudwatch_log_group.this.name
  filter_pattern  = var.metric_filter_pattern
  destination_arn = aws_lambda_function.filter.arn
  distribution    = "ByLogStream"
}