# Free Aws Ec2 Instance by Cdk


In my previous [Free (almost) Aws Ec2 Instance](../free-aws-ec2-instance) blog, I used Aws Cli. It's good for learning, but in the real world, you need to keep creating/deleting it to save cost. Let's make is easy by using CDK.

## app.py

```python
#!/usr/bin/env python3

import aws_cdk as cdk
from cdk.cdk_stack import CdkStack

app = cdk.App()
env = cdk.Environment(
    account="xxxxxxxxxxxx",
    region="us-east-1",
)
CdkStack(app, "cdk", env=env)

app.synth()
```

## cdk/cdk_stack.py
这里用到的 user_data.txt与[Free (almost) Aws Ec2 Instance](../free-aws-ec2-instance) 中创建的相同。

```python
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2
)
from constructs import Construct

# 从user_data.txt 文件读出 user_data
with open('user_data.txt') as f:
    user_data = f.read()

class CdkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Find the Default VPC
        default_vpc = ec2.Vpc.from_lookup(
            self, "DefaultVpc", 
            is_default=True
        )

        # Found the latest debian 11 arm64 AMI which could be launched as t4g.small 
        image = ec2.LookupMachineImage(
            owners = ['amazon'],
            name = 'debian-11-arm64*',
            filters={
                'virtualization-type': ['hvm'],
                'architecture': ['arm64']
            },
        )

        # Found the latest ubuntu 24 arm64 AMI
        # image = ec2.LookupMachineImage(
        #     owners=['099720109477'],  # Canonical 的 AWS 账户 ID
        #     name='ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-arm64-server-*',  # Ubuntu 24 ARM64 的 AMI 名称模式
        #     filters={
        #         'virtualization-type': ['hvm'],
        #         'architecture': ['arm64']
        #     },
        # )
        
        # Create an IAM role for SSM
        ssm_role = iam.Role(self, "SSMInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")]
        )

        # Create an instance profile and add the role to it
        ssm_profile = iam.CfnInstanceProfile(self, "SSMInstanceProfile",
            roles=[ssm_role.role_name]
        )

        # 创建一个EC2实例, 给公共IP吧
        instance = ec2.Instance(
            self, "MyInstance",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE4_GRAVITON, ec2.InstanceSize.SMALL),
            vpc=default_vpc,
            machine_image=image,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            user_data=ec2.UserData.custom(user_data),
            role=ssm_role
        )
```

## Create and destroy

```bash
source .venv/bin/activate
cdk deploy --profile <your profile with access to account="xxxxxxxxxxxx" above >
cdk destroy --profile <your profile with access to account="xxxxxxxxxxxx" above >
```

