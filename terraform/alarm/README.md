<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | n/a |
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_log_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_metric_filter.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_metric_filter) | resource |
| [aws_cloudwatch_metric_alarm.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_metric_alarm) | resource |
| [aws_iam_policy.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_policy_attachment.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy_attachment) | resource |
| [aws_iam_role.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_lambda_function.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [aws_sns_topic.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic) | resource |
| [aws_sns_topic_subscription.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_subscription) | resource |
| [archive_file.this](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_cloudwatch_log_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/cloudwatch_log_group) | data source |
| [aws_iam_policy_document.log](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_actions_enabled"></a> [actions\_enabled](#input\_actions\_enabled) | enabled alarm action | `bool` | `true` | no |
| <a name="input_alarm_description"></a> [alarm\_description](#input\_alarm\_description) | description for this alarm. | `string` | `"Cloud Inventory Alarm"` | no |
| <a name="input_alarm_name"></a> [alarm\_name](#input\_alarm\_name) | name of the alarm | `string` | `"cloud-inventory-alarm"` | no |
| <a name="input_cloudwatch_log_group_name"></a> [cloudwatch\_log\_group\_name](#input\_cloudwatch\_log\_group\_name) | cloudwatch log group name | `string` | n/a | yes |
| <a name="input_comparison_operator"></a> [comparison\_operator](#input\_comparison\_operator) | arithmetic operation to use when comparing the specified Statistic and Threshold. | `string` | `"GreaterThanOrEqualToThreshold"` | no |
| <a name="input_datapoints_to_alarm"></a> [datapoints\_to\_alarm](#input\_datapoints\_to\_alarm) | the number of data points that will trigger alarm | `number` | `3` | no |
| <a name="input_evaluation_periods"></a> [evaluation\_periods](#input\_evaluation\_periods) | the number of periods over which data is compared. | `number` | `5` | no |
| <a name="input_lambda_function_name"></a> [lambda\_function\_name](#input\_lambda\_function\_name) | name of this lambda function | `string` | `"cloud-inventory-slack-notification"` | no |
| <a name="input_lambda_role_name"></a> [lambda\_role\_name](#input\_lambda\_role\_name) | name of the lambda role | `string` | `"cloud-inventory-alarm-lambda-role"` | no |
| <a name="input_metric_filter_name"></a> [metric\_filter\_name](#input\_metric\_filter\_name) | name of the this metric filter | `string` | `"cloud-inventory-filter"` | no |
| <a name="input_metric_filter_pattern"></a> [metric\_filter\_pattern](#input\_metric\_filter\_pattern) | pattern to match | `string` | `"error"` | no |
| <a name="input_metric_transformation_default_value"></a> [metric\_transformation\_default\_value](#input\_metric\_transformation\_default\_value) | default value if no pattern matched | `string` | `null` | no |
| <a name="input_metric_transformation_name"></a> [metric\_transformation\_name](#input\_metric\_transformation\_name) | name cloudwatch metric to store our log events | `string` | `"CloudInventoryError"` | no |
| <a name="input_metric_transformation_namespace"></a> [metric\_transformation\_namespace](#input\_metric\_transformation\_namespace) | namespace for the metric name above | `string` | `"CloudInventoryErrorMetric"` | no |
| <a name="input_metric_transformation_value"></a> [metric\_transformation\_value](#input\_metric\_transformation\_value) | how many occurence of the metric pattern | `string` | `"5"` | no |
| <a name="input_period"></a> [period](#input\_period) | the period in seconds over which the specified statistic is applied. | `string` | `"60"` | no |
| <a name="input_slack_channel_name"></a> [slack\_channel\_name](#input\_slack\_channel\_name) | slack channel name | `string` | `"devops"` | no |
| <a name="input_slack_endpoint_url"></a> [slack\_endpoint\_url](#input\_slack\_endpoint\_url) | slack endpoint url | `string` | `""` | no |
| <a name="input_sns_topic_name"></a> [sns\_topic\_name](#input\_sns\_topic\_name) | sns topic name | `string` | `"cloud-inventory-lambda-invocation"` | no |
| <a name="input_statistic"></a> [statistic](#input\_statistic) | specify the stats to use -e.g Sum, Average, etc | `string` | `"Sum"` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate to this resource | `map(string)` | `{}` | no |
| <a name="input_threshold"></a> [threshold](#input\_threshold) | the value against which the specified statistic is compared. | `number` | `3` | no |
| <a name="input_treat_missing_data"></a> [treat\_missing\_data](#input\_treat\_missing\_data) | specify how to treat missing data points | `string` | `"missing"` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->