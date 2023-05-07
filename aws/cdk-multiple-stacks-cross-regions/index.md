# Cdk Multiple Stacks Cross Regions


## How to create multiple stacks in same CDK program

```python
#!/usr/bin/env python3
import os as os
import aws_cdk as cdk
from cdk.cdk_stack import CdkStack

app = cdk.App()

env_EU = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region="eu-west-1")
env_US = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region="us-east-1")

CdkStack(app, "us", env=env_US)
CdkStack(app, "uk", env=env_EU)

app.synth()
```

The result should be like this:
```bash
$ aws cloudformation --profile dec list-stacks  --region us-east-1 \
    --query 'StackSummaries[].StackName' --stack-status-filter CREATE_COMPLETE
[
    "cdk",
    "CDKToolkit"
]
$ aws cloudformation --profile dec list-stacks  --region eu-west-1 \
    --query 'StackSummaries[].StackName' --stack-status-filter CREATE_COMPLETE
[
    "cdkStandby",
    "CDKToolkit"
]
```
but there are a couple of Requirements.

## Requirements

Follow [AWS official instruction](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html#sts-regions-activate-deactivate) and active STS in your desired region to solve the following error.
```  
Deployment failed: Error: Stack Deployments Failed: ValidationError: 
Role arn:aws:iam::123456789012:role/cdk-hnb659fds-cfn-exec-role-123456789012-eu-west-1 
cannot be used due to Security Token Service (STS) being disabled for the region. 
To use IAM Roles with CloudFormation please enable STS for the region in IAM Account Settings.
```
You might not have bootstrap in all involved regions, there should be CDKToolkit stack in all of them.
Run the bootstrap command again will bootstrap on those regions hadn't been done before.

```bash
cdk bootstrap --profile dec  
```
There might be global resources, like IAM role in each stack. It's not ideal, but shouldn't be a show stopper.

```bash
cdk deploy --all --profile dec
cdk destroy --all --profile dec
```
