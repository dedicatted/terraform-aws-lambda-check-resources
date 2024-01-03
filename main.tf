resource "aws_lambda_function" "existing_resource_function" {
  function_name = var.function_name
  handler       = var.handler
  runtime       = var.runtime
  timeout       = var.timeout

  filename         = var.filename
  role = aws_iam_role.lambda_execution_role.arn
  environment {
    variables = {
      WEBHOOK_URL = var.chat_webhook
    }
  }
}


resource "aws_iam_role" "lambda_execution_role" {
  name = var.lambda_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com",
        },
      },
    ],
  })
}

resource "aws_iam_role_policy" "inline_policy" {
  name   = "LambdaCustomInlinePolicy"
  role   = aws_iam_role.lambda_execution_role.name
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "VisualEditor0",
        Effect = "Allow",
        Action = [
          "ec2:DescribeInternetGateways",
          "ec2:DescribeInstances",
          "ec2:DescribeVpcs",
          "ec2:DescribeVolumes",
          "redshift:DescribeClusters",
          "rds:DescribeDBInstances",
          "ec2:DescribeNatGateways",
          "eks:ListClusters",
          "eks:DescribeCluster",
          "elasticache:DescribeCacheClusters",
          "ecs:ListClusters",
        ],
        Resource = "*",
      },
    ],
  })
}

resource "aws_cloudwatch_event_rule" "lambda_trigger_rule" {
  name        = var.event_rule_name
  description = "Scheduled rule for Lambda execution"
  schedule_expression = var.schedule_expression
  depends_on = [aws_lambda_function.existing_resource_function]
}

resource "aws_cloudwatch_event_target" "event_target" {
  rule      = aws_cloudwatch_event_rule.lambda_trigger_rule.name
  target_id = var.event_target_name
  arn = aws_lambda_function.existing_resource_function.arn
}

resource "aws_lambda_permission" "allow_events_bridge_to_run_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.existing_resource_function.function_name
    principal = "events.amazonaws.com"
}