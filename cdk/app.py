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
