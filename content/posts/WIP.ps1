
DM=$(aws route53domains list-domains --query 'Domains[].DomainName' --output text)
ZONE=$(aws route53 create-hosted-zone --name $DM \
    --caller-reference `date '+%Y-%m-%d-%H-%M-%S'` \
    --query 'HostedZone.Id' --output text)
aws route53 delete-hosted-zone --id $ZONE

aws elbv2 create-target-group --name my-target-group --protocol HTTP --port 80 --vpc-id your-vpc-id
aws elbv2 register-targets --target-group-arn arn:aws:elasticloadbalancing:region:account-id:targetgroup/my-target-group/1234567890abcdef --targets Id=i-1234567890abcdef
aws elbv2 create-load-balancer --name my-load-balancer --subnets subnet-12345678 subnet-abcdef01 --security-groups sg-12345678 --type application
aws elbv2 create-listener --load-balancer-arn arn:aws:elasticloadbalancing:region:account-id:loadbalancer/my-load-balancer/1234567890abcdef --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:region:account-id:targetgroup/my-target-group/1234567890abcdef


With AWS CodePipeline, there are no upfront fees or commitments. You pay only for what you use. AWS CodePipeline costs $1.00 per active pipeline* per month. 
As part of the AWS Free Tier, AWS CodePipeline offers new and existing customers one free active pipeline each month.


Free Tier
The AWS CodeBuild free tier includes 100 total build minutes per month with the general1.small or arm1.small instance types. The CodeBuild free tier does not expire automatically at the end of your 12-month AWS Free Tier term. It is available to new and existing AWS customers.

