# Cdk Free Ec2 in Special Subnet Sg


Based on ["Free Aws Ec2 Instance by Cdk"](../free-aws-ec2-instance-by-cdk), let's change it so it will create and free EC2 instance in a special VPC, subnet and Security Group. This is good for network conectivity testing.

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

# Hardcoded the location and security group of this EC2 instance
subnet_id = "subnet-xxxxxxxxxxxxxxxx"  # Replace with your actual subnet ID
availability_zone = "us-east-1a"  # Replace with your actual availability zone
sg_id = "sg-xxxxxxxxxxxxx"  # Replace with your actual security group ID
vpc_id = "vpc-xxxxxxxxxxxxxx"  # Replace with your actual VPC ID

# Instantiate the stack with subnet_id, availability_zone, sg_id, and vpc_id
CdkStack(app, "cdk", env=env, subnet_id=subnet_id, sg_id=sg_id, availability_zone=availability_zone, vpc_id=vpc_id)

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

    def __init__(self, scope: Construct, id: str, subnet_id: str, sg_id: str, vpc_id: str, availability_zone: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

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

        # Import the subnet with availability zone
        subnet = ec2.Subnet.from_subnet_attributes(self, "Subnet",
            subnet_id=subnet_id,
            availability_zone=availability_zone
        )

        # Import the VPC by its ID (use VPC ID)
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)

        # 创建一个EC2实例, 给公共IP吧
        instance = ec2.Instance(
            self, "testing-ec2",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE4_GRAVITON, ec2.InstanceSize.SMALL),
            machine_image=image,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=[subnet]),
            security_group=ec2.SecurityGroup.from_security_group_id(self, "SecurityGroup", sg_id),
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

