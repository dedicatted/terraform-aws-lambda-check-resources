variable "region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region to deploy."
}

variable "function_name" {
  type        = string
  default     = "AWSResourceChecker"
  description = "Lambda function name. Used to send notifications of existing resources in AWS account to Google chat or other services using API."
}

variable "runtime" {
  type        = string
  default     = "python3.11"
  description = "Lambda function runtime. Must be nodejs as Lambda code is written on nodejs."
}

variable "handler" {
  type        = string
  default     = "lambda_function.lambda_handler"
  description = "Lambda function handler. Must be 'lambda_function.lambda_handler' unless you change it in Lambda code."
}

variable "filename" {
  type        = string
  default     = "lambda_handler.zip"
  description = "ZIP archive with Lambda code. Must be 'lambda_handler.zip' unless you change the archive name."
}

variable "lambda_role_name" {
  type        = string
  default     = "existing-resource-notificator-lambda-role"
  description = "Lambda IAM role name."
}

variable "chat_webhook" {
  type        = string
  default     = "https://chat.googleapis.com/v1/spaces/"
  description = "Webhook url where to send notifications"
}

variable "timeout" {
  type = number
  default = 30
  description = "Time limite of lambda execution"
}

variable "event_rule_name" {
  type = string
  default = "LambdaTrigger"
  description = "Name of cloudwatch event rule for trigger lambda using schedule"
}

variable "schedule_expression" {
  type = string
  default = "cron(0 16 * * ? *)"
  description = "Cron exception to define lambda trigger time"
}

variable "event_target_name" {
  type = string
  default = "LambdaTargetName"
  description = "Name of cloud watch event target"
}