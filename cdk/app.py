#!/usr/bin/env python3
import os as os
import aws_cdk as cdk
from cdk.cdk_stack import CdkStack
from cdk.cdk_dns import MyStack

app = cdk.App()

env_EU = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region="eu-west-1")
env_US = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region="us-east-1")

cdk_us = CdkStack(app, "us", env=env_US)
cdk_uk = CdkStack(app, "uk", env=env_EU)

# 导入输出值
EU_publicip = cdk.Fn.import_value(
    "cdk_uk:publicip"
)
print(EU_publicip)

US_publicip = cdk.Fn.import_value(
    "cdk_us:publicip"
)
print(US_publicip)

MyStack(app, "dns",
        domain_name="victorma.net"
)

app.synth()
