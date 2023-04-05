# Dns From Name Tag


## Create Route53 records based on EC2 Tags.Name


1. There might have duplicated Tags.Name, so array is used to pick them up and manipulate.
1. Tags.Name might include charactors not qualified for dns name, regular expression is used to remove them.
1. There might be no Tags.Name, next()函数and返回生成器is used.

```python
import boto3
import re
import json

session = boto3.Session()
ec2 = session.client('ec2')
route53_client = boto3.client('route53')

HOSTED_ZONE_ID = "REPLACE WITH YOUR ZONE ID"
ZONE = ".example.com"

# 获取所有运行中的实例
response = ec2.describe_instances(Filters=[
    {'Name': 'instance-state-name', 'Values': ['running']}
])

# 用于存储实例标签的字典, 检测相同名字的list
instance_dict = {}
dns_names = []

# 遍历每个实例，获取实例ID和标签
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        private_ip = instance['PrivateIpAddress']
        tags = instance.get('Tags', [])
        # 生成器tag for tag in tags if tag['Key'] == 'Name'是一种可迭代对象，可以逐个地产生值，而不必等待所有值都生成
        # next()函数返回生成器的下一个值，并将生成器的内部指针向前移动。如果没有更多的值可以生成，next()函数将引发StopIteration异常。
        # 从标签列表tags中获取Key为'Name'的标签对象。如果找到了这样的标签，则next()函数返回该标签对象；否则，它将返回None
        # 该标签对象是一个字典，其包含'Key'为'Name'的键和对应的'Value'
        # 如果生成器表达式没有找到匹配的标签，则name_tag将是NoneType。
        name_tag = next((tag for tag in tags if tag['Key'] == 'Name'), None)
        # 如果name_tag是一个标签字典，则可以使用name_tag['Value']来获取实例的名称。 name是string
        name = name_tag['Value'] if name_tag else 'no-tag'
        
        # 构造DNS名称
        # 删除括号及其内部内容
        dns_name = re.sub(r'\([^)]*\)', '', name)
        # 删除行尾的“server”或“Server”
        dns_name = re.sub(r'(-)?[Ss]erver$', '', dns_name)
        # 删除行尾的“DONOTSTART”
        dns_name = re.sub(r'DONOTSTART', '', dns_name)
        # 删除行尾的“-”字符
        dns_name = re.sub(r'[-\s]+$', '', dns_name)
        # 将空格替换为“-”
        dns_name = re.sub(r'\s+', '-', dns_name)
        # 如果DNS名称已经存在，添加数字
        count = 1
        while dns_name in dns_names:
            count += 1
            dns_name = re.sub(r'(-\d+)?$', '-' + str(count), dns_name)
        dns_names.append(dns_name)
        # 加上你自己的域名
        dns_name += ZONE

        # Register the DNS record
        response = route53_client.change_resource_record_sets(
            HostedZoneId= HOSTED_ZONE_ID,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': dns_name,
                            'Type': 'A',
                            'TTL': 300,
                            'ResourceRecords': [
                                {
                                    'Value': private_ip
                                }
                            ]
                        }
                    }
                ]
            }
        )
        change_info = response['ChangeInfo']
        status = change_info['Status']
        
        # 将实例ID，标签和DNS名称添加到字典中
        instance_dict[instance_id] = {'private_ip': private_ip, 'status': status, 'dns_name': dns_name, 'name': name}

# 打印字典中的所有实例
for instance_id, instance_info in instance_dict.items():
    dns_name = instance_info['dns_name']
    name = instance_info['name']
    private_ip = instance_info['private_ip']
    status = instance_info['status']
    print(f"{instance_id} : {status } : {private_ip} : {dns_name} : {name}")
```
