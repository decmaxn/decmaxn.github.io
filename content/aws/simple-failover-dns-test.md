---
title: "Simple Failover Dns Test"
date: 2023-04-17T10:24:40-04:00
draft: false
tags: ["cdk", "AWS", "tips"]
---

## Test failover DNS 

Based on [Cdk Multiple Stacks Cross Regions](../cdk-multiple-stacks-cross-regions), we created 2 web servers in 2 regions. Now let's create a failover DNS records and test it's feature.

### Create 2 web servers in 2 regions, and a hosted zone
You need to have a registered domain. In my case, it's victorma.net. First of all, I added a stack to create a hosted zone.

Append the following to app.py
```python
from cdk.cdk_dns import MyStack

MyStack(app, "dns",
        domain_name="victorma.net"
)
```
Create cdk_dns.py in cdk folder.
```python
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
```
### Test it out
After cdk deploy, let's verify resources been created first.
```bash
aws ec2 describe-instances --profile dec --region eu-west-1
aws ec2 describe-instances --profile dec --region us-east-1

EUIP=$(aws ec2 describe-instances \
    --profile dec --region eu-west-1 --output text \
    --query "Reservations[].Instances[0].PublicIpAddress")
USIP=$(aws ec2 describe-instances \
    --profile dec --region us-east-1 --output text \
    --query "Reservations[].Instances[0].PublicIpAddress")

aws route53 list-health-checks \
    --profile dec --output text \
    --query "HealthChecks[*].{ID:Id, Name:HealthCheckConfig.IPAddress}"

aws route53 --profile dec list-hosted-zones
ZONE=$(aws route53 list-hosted-zones \
    --profile dec --output text \
    --query "HostedZones[0].Id")

NSS=$(aws route53 get-hosted-zone \
     --profile dec --output text \
    --id $ZONE \
    --query 'DelegationSet.NameServers')
```
Update NS records of registered domain to the new Zone's NS records
```bash
aws route53domains get-domain-detail \
    --profile dec  \
    --domain-name victorma.net \
    --query "Nameservers"
FNSS=$(for x in $NSS; do echo -n "Name=$x "; done)
aws route53domains update-domain-nameservers \
    --profile dec  --region us-east-1 \
    --domain-name victorma.net --nameservers $FN
```

Create failover.json to create failover records  

```bash
# the IP and HealthCheckId should match the health check result above
cat > failover.json <<EOF
{
    "Changes": [
        {
        "Action": "DELETE",
        "ResourceRecordSet": 
            {
                "Name": "mytet.victorma.net",
                "Type": "A",
                "SetIdentifier": "eu",
                "Failover": "PRIMARY",
                "TTL": 10,
                "ResourceRecords": [
                    {
                        "Value": "54.229.174.252"
                    }
                ],
                "HealthCheckId": "609e50ff-b807-40c7-b938-bffa93f735d5"
            }
        },
        {
        "Action": "DELETE",
        "ResourceRecordSet": 
            {
                "Name": "mytest.victorma.net",
                "Type": "A",
                "SetIdentifier": "eu",
                "Failover": "SECONDARY",
                "TTL": 10,

                
                "ResourceRecords": [
                    {
                        "Value": "52.91.241.122"
                    }
                ],
                "HealthCheckId": "b7b70a57-f84a-41ab-b3ec-312e7c652496"
            }
        }
    ]
}
EOF

# check and create the failover DNS records
aws route53 --profile dec list-resource-record-sets --hosted-zone-id $ZONE
aws route53 --profile dec change-resource-record-sets --hosted-zone-id $ZONE \
    --change-batch file://failover.json
```


# remove the failover DNS records to prepare for cdk destroy



