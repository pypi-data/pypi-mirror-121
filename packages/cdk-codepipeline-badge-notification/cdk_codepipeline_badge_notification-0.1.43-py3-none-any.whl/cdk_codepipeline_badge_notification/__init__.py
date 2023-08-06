'''
[![NPM version](https://badge.fury.io/js/cdk-pipeline-status.svg)](https://badge.fury.io/js/cdk-pipeline-status)
[![PyPI version](https://badge.fury.io/py/cdk-pipeline-status.svg)](https://badge.fury.io/py/cdk-pipeline-status)
[![Release](https://github.com/kimisme9386/cdk-codepipeline-status/actions/workflows/release.yml/badge.svg)](https://github.com/kimisme9386/cdk-codepipeline-status/actions/workflows/release.yml)

# CDK-CodePipeline-Status

## Feature

* Generate badge when AWS CodePipeline state change
* Update GitHub commit status when AWS CodePipeline state change
* Slack notification when AWS CodePipeline state change

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_pipeline_status import CodePipelineStatus
import aws_cdk.core as cdk
import aws_cdk.aws_codepipeline as code_pipeline

app = cdk.App()
env = {
    "region": process.env.CDK_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}
stack = cdk.Stack(app, "codepipeline-status", env=env)

pipeline = code_pipeline.Pipeline(stack, "TestPipeline",
    pipeline_name="testCodePipeline",
    cross_account_keys=False
)

CodePipelineStatus(stack, "CodePipelineStatus",
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
CodePipelineStatus(stack, "CodePipelineStatus",
    pipeline_arn=pipeline.pipeline_arn
)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class CodePipelineStatus(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-codepipeline-badge-notification.CodePipelineStatus",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        pipeline_arn: builtins.str,
        git_hub_token_from_secrets_manager: typing.Optional["GitHubTokenFromSecretsManager"] = None,
        notification: typing.Optional["Notification"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param pipeline_arn: (experimental) AWS CodePipeline arn.
        :param git_hub_token_from_secrets_manager: (experimental) AWS Secret Manager id or arn.
        :param notification: (experimental) Notification.

        :stability: experimental
        '''
        props = CodePipelineStatusProps(
            pipeline_arn=pipeline_arn,
            git_hub_token_from_secrets_manager=git_hub_token_from_secrets_manager,
            notification=notification,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="badgeUrl")
    def badge_url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "badgeUrl"))

    @badge_url.setter
    def badge_url(self, value: builtins.str) -> None:
        jsii.set(self, "badgeUrl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="codePipelineLink")
    def code_pipeline_link(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "codePipelineLink"))

    @code_pipeline_link.setter
    def code_pipeline_link(self, value: builtins.str) -> None:
        jsii.set(self, "codePipelineLink", value)


@jsii.data_type(
    jsii_type="cdk-codepipeline-badge-notification.CodePipelineStatusProps",
    jsii_struct_bases=[],
    name_mapping={
        "pipeline_arn": "pipelineArn",
        "git_hub_token_from_secrets_manager": "gitHubTokenFromSecretsManager",
        "notification": "notification",
    },
)
class CodePipelineStatusProps:
    def __init__(
        self,
        *,
        pipeline_arn: builtins.str,
        git_hub_token_from_secrets_manager: typing.Optional["GitHubTokenFromSecretsManager"] = None,
        notification: typing.Optional["Notification"] = None,
    ) -> None:
        '''
        :param pipeline_arn: (experimental) AWS CodePipeline arn.
        :param git_hub_token_from_secrets_manager: (experimental) AWS Secret Manager id or arn.
        :param notification: (experimental) Notification.

        :stability: experimental
        '''
        if isinstance(git_hub_token_from_secrets_manager, dict):
            git_hub_token_from_secrets_manager = GitHubTokenFromSecretsManager(**git_hub_token_from_secrets_manager)
        if isinstance(notification, dict):
            notification = Notification(**notification)
        self._values: typing.Dict[str, typing.Any] = {
            "pipeline_arn": pipeline_arn,
        }
        if git_hub_token_from_secrets_manager is not None:
            self._values["git_hub_token_from_secrets_manager"] = git_hub_token_from_secrets_manager
        if notification is not None:
            self._values["notification"] = notification

    @builtins.property
    def pipeline_arn(self) -> builtins.str:
        '''(experimental) AWS CodePipeline arn.

        :stability: experimental
        '''
        result = self._values.get("pipeline_arn")
        assert result is not None, "Required property 'pipeline_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def git_hub_token_from_secrets_manager(
        self,
    ) -> typing.Optional["GitHubTokenFromSecretsManager"]:
        '''(experimental) AWS Secret Manager id or arn.

        :stability: experimental
        '''
        result = self._values.get("git_hub_token_from_secrets_manager")
        return typing.cast(typing.Optional["GitHubTokenFromSecretsManager"], result)

    @builtins.property
    def notification(self) -> typing.Optional["Notification"]:
        '''(experimental) Notification.

        :stability: experimental
        '''
        result = self._values.get("notification")
        return typing.cast(typing.Optional["Notification"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodePipelineStatusProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-codepipeline-badge-notification.GitHubTokenFromSecretsManager",
    jsii_struct_bases=[],
    name_mapping={
        "secret_key": "secretKey",
        "secrets_manager_arn": "secretsManagerArn",
    },
)
class GitHubTokenFromSecretsManager:
    def __init__(
        self,
        *,
        secret_key: typing.Optional[builtins.str] = None,
        secrets_manager_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_key: (experimental) SecretKey.
        :param secrets_manager_arn: (experimental) Arn with other type of secrets.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if secrets_manager_arn is not None:
            self._values["secrets_manager_arn"] = secrets_manager_arn

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) SecretKey.

        :stability: experimental
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_manager_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Arn with other type of secrets.

        :stability: experimental
        '''
        result = self._values.get("secrets_manager_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubTokenFromSecretsManager(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-codepipeline-badge-notification.Notification",
    jsii_struct_bases=[],
    name_mapping={"slack_web_hook_url": "slackWebHookUrl", "stage_name": "stageName"},
)
class Notification:
    def __init__(
        self,
        *,
        slack_web_hook_url: typing.Optional[builtins.str] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param slack_web_hook_url: (experimental) Slack webhook url.
        :param stage_name: (experimental) Prefix title for slack message.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if slack_web_hook_url is not None:
            self._values["slack_web_hook_url"] = slack_web_hook_url
        if stage_name is not None:
            self._values["stage_name"] = stage_name

    @builtins.property
    def slack_web_hook_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Slack webhook url.

        :stability: experimental
        '''
        result = self._values.get("slack_web_hook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix title for slack message.

        :stability: experimental
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Notification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CodePipelineStatus",
    "CodePipelineStatusProps",
    "GitHubTokenFromSecretsManager",
    "Notification",
]

publication.publish()
