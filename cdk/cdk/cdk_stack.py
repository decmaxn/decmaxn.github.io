from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # # Find Default VPC
        default_vpc = ec2.Vpc.from_lookup(
            self, "DefaultVpc", 
            is_default=True
        )


        # 创建一个安全组
        security_group = ec2.SecurityGroup(
            self, "MySecurityGroup",
            vpc=default_vpc,
            allow_all_outbound=True
        )

        # 添加Inbound规则
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22)
        )

        image = ec2.LookupMachineImage(
            owners = ['amazon'],
            name = 'debian-11-arm64*',
            filters={
                'virtualization-type': ['hvm'],
                'architecture': ['arm64']
            },
        )

        # 创建一个EC2实例, 给公共IP吧
        instance = ec2.Instance(
            self, "MyInstance",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE4_GRAVITON, ec2.InstanceSize.SMALL),
            vpc=default_vpc,
            machine_image=image,
            security_group=security_group,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            user_data=ec2.UserData.custom("#!/bin/bash\necho 'Hello, World!' > index.html\nnohup python -m SimpleHTTPServer 80 &")
        )