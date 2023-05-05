from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2
)
from constructs import Construct

# 读出一个文件中的user_data
with open('user_data.txt') as f:
    user_data = f.read()

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
            connection=ec2.Port.tcp(80)
        )

        image = ec2.LookupMachineImage(
            owners = ['amazon'],
            name = 'debian-11-arm64*',
            filters={
                'virtualization-type': ['hvm'],
                'architecture': ['arm64']
            },
        )

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
            security_group=security_group,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            user_data=ec2.UserData.custom(user_data),
            role=ssm_role
        )