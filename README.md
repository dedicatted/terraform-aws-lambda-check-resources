# Terraform Module: terraform-aws-lambda
# This module facilitates the creation of AWS Budgets with flexible notification options, including email, Slack, and Google Chat.

## Overview
The `terarform-aws-lambda` module enables you to easily deploy AWS Lambda fucntion which helping you monitor and control your AWS existing resources. The module supports multiple notification channels, allowing you to receive alerts through any API.

## Usage
If you want to cange lambda function, check lambda_function.py
```hcl
//Configuration for Google chat webhook
module lambda_notify {
  source = "github.com/dedicatted/terraform-lambda-notify"
  chat_webhook = "/v1/spaces/space/messages?key=key&token=token"
}
```



## How to create Google chat webhook

 - In a browser, open Chat. Webhooks aren't configurable from the Chat mobile app.
 - Go to the space where you want to add a webhook.
 - Next to the space title, click the expand_more expand more arrow, and then click Apps & integrations.
 - Click addAdd webhooks.
 - In the Name field, enter Quickstart Webhook.
 - (Optional) In the Avatar URL field, enter https://developers.google.com/chat/images/chat-product-icon.png.
 - Click Save.
 - To copy the webhook URL, click more_vert More, and then click content_copyCopy link.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.30.0 |

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_event_rule.lambda_trigger_rule](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.event_target](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_iam_role.lambda_execution_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy.inline_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_lambda_function.existing_resource_function](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.allow_events_bridge_to_run_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_chat_webhook"></a> [chat\_webhook](#input\_chat\_webhook) | Webhook url where to send notifications | `string` |  | yes |
| <a name="input_event_rule_name"></a> [event\_rule\_name](#input\_event\_rule\_name) | Name of cloudwatch event rule for trigger lambda using schedule | `string` | `"LambdaTrigger"` | no |
| <a name="input_event_target_name"></a> [event\_target\_name](#input\_event\_target\_name) | Name of cloud watch event target | `string` | `"LambdaTargetName"` | no |
| <a name="input_filename"></a> [filename](#input\_filename) | ZIP archive with Lambda code. Must be 'lambda\_handler.zip' unless you change the archive name. | `string` | `"lambda_handler.zip"` | no |
| <a name="input_function_name"></a> [function\_name](#input\_function\_name) | Lambda function name. Used to send notifications of existing resources in AWS account to Google chat or other services using API. | `string` | `"AWSResourceChecker"` | no |
| <a name="input_handler"></a> [handler](#input\_handler) | Lambda function handler. Must be 'lambda\_function.lambda\_handler' unless you change it in Lambda code. | `string` | `"lambda_function.lambda_handler"` | no |
| <a name="input_lambda_role_name"></a> [lambda\_role\_name](#input\_lambda\_role\_name) | Lambda IAM role name. | `string` | `"existing-resource-notificator-lambda-role"` | no |
| <a name="input_region"></a> [region](#input\_region) | AWS region to deploy. | `string` | `"us-east-1"` | no |
| <a name="input_runtime"></a> [runtime](#input\_runtime) | Lambda function runtime. Must be nodejs as Lambda code is written on nodejs. | `string` | `"python3.11"` | no |
| <a name="input_schedule_expression"></a> [schedule\_expression](#input\_schedule\_expression) | Cron exception to define lambda trigger time | `string` | `"cron(0 16 * * ? *)"` | no |
| <a name="input_timeout"></a> [timeout](#input\_timeout) | Time limite of lambda execution | `number` | `30` | no |
