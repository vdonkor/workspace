module "alarm" {
  source = "./alarm"
  cloudwatch_log_group_name = "/ecs/bento/dev/logs"
  slack_endpoint_url = "slack-endpoint-url"
  sns_topic_name  = "sns-topic-name"
  lambda_function_name = "lambda-function-name"
  slack_channel_name = "slack-channel-name"
  metric_filter_pattern = "error"
  metric_filter_name = "metric-filter-name"
  metric_transformation_namespace = "namespace-name"
  metric_transformation_name = "metric-transformation-name"
  alarm_name = "alarm-name"
  alarm_description = "alarm-description"
  evaluation_periods = 5
  threshold = 3
  statistic = "Sum"
  datapoints_to_alarm = 2
  comparison_operator = "GreaterThanOrEqualToThreshold"
  period = "60"
  slack_bot_user_ouath_token = ""
  slack_files_upload_endpoint_url = ""
}