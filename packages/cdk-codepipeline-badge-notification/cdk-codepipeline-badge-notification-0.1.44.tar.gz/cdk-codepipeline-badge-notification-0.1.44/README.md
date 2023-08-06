[![NPM version](https://badge.fury.io/js/cdk-codepipeline-badge-notification.svg)](https://badge.fury.io/js/cdk-codepipeline-badge-notification)
[![PyPI version](https://badge.fury.io/py/cdk-codepipeline-badge-notification.svg)](https://badge.fury.io/py/cdk-codepipeline-badge-notification)
[![Release](https://github.com/kimisme9386/cdk-codepipeline-badge-notification/actions/workflows/release.yml/badge.svg)](https://github.com/kimisme9386/cdk-codepipeline-badge-notification/actions/workflows/release.yml)

# CDK-CodePipeline-Badge-Notification

## Feature

* Generate badge when AWS CodePipeline state change
* Update GitHub commit status when AWS CodePipeline state change
* Slack notification when AWS CodePipeline state change

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_pipeline_badge_notification import CodePipelineBadgeNotification
import aws_cdk.core as cdk
import aws_cdk.aws_codepipeline as code_pipeline

app = cdk.App()
env = {
    "region": process.env.CDK_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}
stack = cdk.Stack(app, "codepipeline-badge-notification", env=env)

pipeline = code_pipeline.Pipeline(stack, "TestPipeline",
    pipeline_name="testCodePipeline",
    cross_account_keys=False
)

CodePipelineBadgeNotification(stack, "CodePipelineBadgeNotification",
    pipeline_arn=pipeline.pipeline_arn,
    git_hub_token_from_secrets_manager={
        "secrets_manager_arn": "arn:aws:secretsmanager:ap-northeast-1:111111111111:secret:codepipeline/lambda/github-token-YWWmII",
        "secret_key": "codepipeline/lambda/github-token"
    },
    notification={
        "stage_name": "production",
        "slack_web_hook_url": "slack url webhook"
    }
)
```

> gitHubTokenFromSecretsManager and notification is optional

#### Only badge

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
CodePipelineBadgeNotification(stack, "CodePipelineBadgeNotification",
    pipeline_arn=pipeline.pipeline_arn
)
```
