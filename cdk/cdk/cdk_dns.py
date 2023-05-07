from aws_cdk import (
    Stack,
    aws_route53 as route53
)
from constructs import Construct


class MyStack(Stack):
    def __init__(self, scope: Construct, id: str, domain_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        zone_id = route53.PublicHostedZone(self, 'MyZone', 
                zone_name=domain_name,
                )