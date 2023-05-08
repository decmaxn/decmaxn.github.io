# Free (almost) Aws Ec2 Instance


## Create a free Linux EC2 instance

Free Trial: Try Amazon EC2 t4g.small instances powered by AWS Graviton2 processors free for up to 750 hours / month until Dec 31st 2023.
https://aws.amazon.com/blogs/aws/new-t4g-instances-burstable-performance-powered-by-aws-graviton2/

Although the instance is free, but I have been charge a few cents per day under category of "EC2 - Other" for type of EBS:VolumeUsage.gp2. There is no free tier or trail for EBS as far as I know.

Found the latest debian 11 arm64 AMI which could be launched as t4g.small 

```bash
LATEST_AMI_NAME=$(aws ec2 describe-images --owners amazon \
    --filters "Name=name,Values=debian-11-arm64*" "Name=virtualization-type,Values=hvm" "Name=architecture,Values=arm64" \
    --query 'sort_by(Images, &CreationDate)[-1].[ImageId]' \
    --output text)
aws ec2 describe-images --image-ids $LATEST_AMI_NAME
```

Create a userData file to initialize the instance with your necessary tools

```bash
cat <<EOF > user_data.txt
#!/bin/bash

# Basics
sudo apt update
sudo apt upgrade -y
sudo apt-get -qy install --no-install-recommends curl wget zip unzip pv jqs

# SSM Agent #
wget https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_arm64/amazon-ssm-agent.deb
sudo dpkg -i amazon-ssm-agent.deb
sudo systemctl status amazon-ssm-agent
sudo systemctl enable amazon-ssm-agent
sudo systemctl start amazon-ssm-agent

# AWS CLI v2 and Git #
sudo apt install git -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

# Python3
sudo apt-get install python3-pip -y
pip install boto3
EOF
```

Find and use a subnet within a VPC

```bash
# Create a IAM policy, role with SSM session manager permission to assign to the new instance
aws iam create-role --role-name "SSMInstanceRole" --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
aws iam attach-role-policy --role-name "SSMInstanceRole" \
  --policy-arn "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
aws iam create-instance-profile \
  --instance-profile-name SSMInstanceProfile
aws iam add-role-to-instance-profile \
  --instance-profile-name SSMInstanceProfile \
  --role-name SSMInstanceRole

# find all VPCs and chose one, etc. the first one
aws ec2 describe-vpcs --query "Vpcs[].VpcId"
VPC=$(aws ec2 describe-vpcs --query "Vpcs[].VpcId" --output text)
# find all subnets, private subnets and choose one. Private one is better, but not necessary.
aws ec2 describe-subnets \
  --query "Subnets[?VpcId==\`$VPC\`].SubnetId"
aws ec2 describe-subnets \
  --query "Subnets[?VpcId==\`$VPC\`] | [?MapPublicIpOnLaunch==\`false\`].SubnetId"
SN=$(aws ec2 describe-subnets \
  --query "Subnets[?VpcId==\`$VPC\`].SubnetId | [0]" \
  --output text)

# Create an EC2 instance which we can use SSM session manager to remote into it
aws ec2 run-instances --image-id $LATEST_AMI_NAME \
  --count 1 --instance-type t4g.small \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=vma-test-2-delete}]' \
  --iam-instance-profile Name=SSMInstanceProfile \
  --key-name vma_rsa \
  --subnet-id $SN \
  --user-data file://user_data.txt
```
## Test using aws cli and ssh
Assume you have aws cli and session manager plugin installed already.
```bash
aws ssm --profile ${AWS_PROFILE} --region ${region}  start-session --target ${InstanceId}
```
Linux: use SSH on top of Session manager 
```bash
$ tail -4 ~/.ssh/config 
# SSH over Session Manager
host i-* mi-*
  ProxyCommand sh -c "aws ssm --profile dec --region us-east-1 start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
  IdentityFile ~/.ssh/vma_rsa
$ ssh admin@i-0fdc88fe37f8af01b
```
Windows: in case you haven't install the Session Manager plugin
```
PS C:\> curl https://s3.amazonaws.com/session-manager-downloads/plugin/latest/windows/SessionManagerPluginSetup.exe -o SessionManagerPluginSetup.exe^C
PS C:\> .\SessionManagerPluginSetup.exe
PS C:\> del .\SessionManagerPluginSetup.exe
```
And the following lines in ~/.ssh/config, test it the same way as in Linux
```
PS C:\> cat ~\.ssh\config
# SSH over Session Manager
host i-* mi-*
  ProxyCommand C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe "aws ssm --profile dec start-session --target %h --document-name AWS-StartSSHSession --parameters portNumber=%p"
  IdentityFile  C:\Users\vma\.ssh\vma_rsa
  User admin
Host i-0fdc88fe37f8af01b
  HostName i-0fdc88fe37f8af01b
```
## Config vscode to use this as remote SSH dev env
1. Install ms-vscode-remote.remote-ssh extension
2. Control+Shift+P, SSH, connect to host
3. Choose the instance ID, etc. i-0fdc88fe37f8af01b

## Clean up
```bash
aws ec2 terminate-instances --instance-ids ${InstanceId}
```

## Misc

```bash
aws ec2 describe-images --owners amazon --filters Name=architecture,Values=arm64 --query 'length(Images[])'
aws ec2 describe-images --owners aws-marketplace --filters Name=architecture,Values=arm64 --query 'length(Images[])'
```

