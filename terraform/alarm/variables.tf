variable "cloudwatch_log_group_name" {
  description = "cloudwatch log group name"
  type = string
}

variable "metric_filter_name" {
  description = "name of the this metric filter"
  type = string
  default = "cloudwatch-metric-filter-name"
}

variable "metric_filter_pattern" {
  description = "pattern to match"
  type = string
  default = "error"
}
variable "metric_transformation_name" {
  description = "name cloudwatch metric to store our log events"
  type        = string
  default = "CloudInventoryError"
}
variable "metric_transformation_namespace" {
  description = "namespace for the metric name above"
  type        = string
  default     =  "CloudInventoryErrorMetric"
}
variable "metric_transformation_value" {
  description = "how many occurence of the metric pattern"
  type        = string
  default     = "5"
}
variable "metric_transformation_unit" {
  description ="metric"
  type        = string
  default     = "5"
}
variable "metric_transformation_default_value" {
  description = "default value if no pattern matched"
  type        = string
  default     = null
}
variable "alarm_name" {
  description = "name of the alarm"
  type        = string
  default     =  "cloud-inventory-alarm"
}

variable "alarm_description" {
  description = "description for this alarm."
  type        = string
  default     = "Cloud Inventory Alarm"
}

variable "evaluation_periods" {
  description = "the number of periods over which data is compared."
  type        = number
  default     =  5
}

variable "threshold" {
  description = "the value against which the specified statistic is compared."
  type        = number
  default     = 3
}

variable "period" {
  description = "the period in seconds over which the specified statistic is applied."
  type        = string
  default     = "60"
}
variable "statistic" {
  description = "specify the stats to use -e.g Sum, Average, etc"
  type        = string
  default     = "Sum"
}
variable "actions_enabled" {
  description = "enabled alarm action"
  type        = bool
  default     = true
}
variable "datapoints_to_alarm" {
  description = "the number of data points that will trigger alarm"
  type        = number
  default     = 3
}
variable "treat_missing_data" {
  description = "specify how to treat missing data points"
  type        = string
  default     = "missing"
}
variable "tags" {
  description = "tags to associate to this resource"
  type        = map(string)
  default     = {}
}
variable "comparison_operator" {
  description = "arithmetic operation to use when comparing the specified Statistic and Threshold."
  type        = string
  default     = "GreaterThanOrEqualToThreshold"
}
variable "lambda_role_name" {
  description = "name of the lambda role"
  type        = string
  default     = "cloudwatch-metric-alarm-lambda-role"
}
variable "slack_channel_name" {
  type = string
  description = "slack channel name"
  default = "devops"
}
variable "lambda_function_name" {
  type = string
  description = "name of this lambda function"
  default = "metric-filter-lambda"
}
variable "sns_topic_name" {
  type = string
  description = "sns topic name"
  default = "cloudwatch-metric-filter-sns-topic"
}
variable "slack_endpoint_url" {
  type = string
  description = "slack endpoint url"
}
