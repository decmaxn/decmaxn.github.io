# Aws Cdk with Python


## Prerequisites

The 2.0 version of CDK is compatible with node 10.19.

```bash
$ aws --version
aws-cli/2.7.13 Python/3.9.11 Linux/5.10.102.1-microsoft-standard-WSL2 exe/x86_64.ubuntu.20 prompt/off
$ aws sts --profile dec 
$ node --version
v10.19.0
$ sudo npm install -g aws-cdk@2.0.0
$ cdk --version
2.0.0 (build 4b6ce31)
$ python3 --version
Python 3.8.10
```
Later on I found Node v10.19.0 has reached end-of-life and is not supported.
```bash
$ sudo npm install n -g
/usr/local/bin/n -> /usr/local/lib/node_modules/n/bin/n
+ n@9.1.0
added 1 package from 2 contributors in 0.442s
$ sudo n stable
$ node --version
v18.16.0
$ sudo npm install -g npm@latest
$ sudo npm --version
9.6.5
$ sudo npm install -g aws-cdk@latest
$ cdk --version
2.76.0 (build 78c411b)
```

## New Sample Project
```bash
$ rm -rf cdk; mkdir cdk; cd cdk
/cdk$ cdk init sample-app --language python
Applying project template sample-app for python

# Welcome to your CDK Python project!

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`cdk_stack`) 
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:
 
$ python3 -m venv .venv 

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.
 
$ source .venv/bin/activate 

If you are a Windows platform, you would activate the virtualenv like this:
 
% .venv\Scripts\activate.bat 

Once the virtualenv is activated, you can install the required dependencies.
 
$ pip install -r requirements.txt 

At this point you can now synthesize the CloudFormation template for this code.
 
$ cdk synth 

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:
 
$ pytest 

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

Please run 'python3 -m venv .venv'!
Executing Creating virtualenv...
✅ All done!
****************************************************
*** Newer version of CDK is available [2.76.0]   ***
*** Upgrade recommended (npm install -g aws-cdk) ***
****************************************************
```
## Test Synthesize and Deploy
```bash
/cdk$ source .venv/bin/activate
(.venv) /cdk$ pip install -r requirements.txt
/cdk$ cdk synth
/cdk$ cdk --profile dec bootstrap
/cdk$ cdk --profile dec deploy
```

## Clean up
Remove the queue, topic and subscription from cdk/cdk_stack.py file, then review by diff and deploy to clean up
```bash
/cdk$ cdk --profile dec diff
Stack cdk
IAM Statement Changes
┌───┬─────────────────────────┬────────┬─────────────────┬───────────────────────────┬─────────────────────────────────────────────────────────┐
│   │ Resource                │ Effect │ Action          │ Principal                 │ Condition                                               │
├───┼─────────────────────────┼────────┼─────────────────┼───────────────────────────┼─────────────────────────────────────────────────────────┤
│ - │ ${CdkQueueBA7F247D.Arn} │ Allow  │ sqs:SendMessage │ Service:sns.amazonaws.com │ "ArnEquals": {                                          │
│   │                         │        │                 │                           │   "aws:SourceArn": "${CdkTopic7E7E1214}"                │
│   │                         │        │                 │                           │ }                                                       │
└───┴─────────────────────────┴────────┴─────────────────┴───────────────────────────┴─────────────────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)

Resources
[-] AWS::SQS::Queue CdkQueueBA7F247D destroy
[-] AWS::SQS::QueuePolicy CdkQueuePolicy9CB1D142 destroy
[-] AWS::SNS::Subscription CdkQueuecdkCdkTopic33B437C257F995AC destroy
[-] AWS::SNS::Topic CdkTopic7E7E1214 destroy
/cdk$ cdk --profile dec deploy
```

## Lambda

Create lambda/hello.py 
```python
import json

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
    }
```
use it to create a lambda function
```yaml
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
...
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='hello.handler',
            code=_lambda.Code.from_asset('lambda'),
        )
```
and diff, deploy
```bash
/cdk$ cdk --profile dec diff
/cdk$ cdk --profile dec deploy
```
Test if it works by Test of the Lambda function or invoke it on AWS

## Hotswap deployments
If possible, the CDK CLI will use AWS service APIs to directly make the changes; otherwise it will fall back to performing a full CloudFormation deployment.
```bash
cdk deploy --hotswap
```
cdk watch is similar to cdk deploy except that instead of being a one-shot operation, it monitors your code and assets for changes and attempts to perform a deployment automatically when a change is detected. 

By default, cdk watch will use the --hotswap flag, which inspects the changes and determines if those changes can be hotswapped. 

Calling cdk watch --no-hotswap will disable the hotswap behavior.

## API Gateway
Put this API gateway in front of the Lambda function. Deploy shows output of it's URL. Curl to test it out.

```python
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=my_lambda,
        )
```

## define a new construct called HitCounter
it will count how many requests were issued to each URL path. It will store this in a DynamoDB table.

Create a new file under cdk_workshop called hitcounter.py 
```python
from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    # RemovalPolicy 是 AWS CDK 中用于指定删除策略的模块。
    RemovalPolicy
)

class HitCounter(Construct):
    # 创建一个名为 handler 的只读属性，返回 _handler 变量的值。
    @property
    def handler(self):
        return self._handler

    # 装饰器使得可以通过调用属性方法的方式来访问这个私有属性
    # 而不是直接访问该属性本身。使得代码更加安全和可维护
    @property
    def table(self):
        # 返回这个私有属性_table的值，从而允许其他代码访问该私有属性的值。
        return self._table
    
    #  构造函数的初始化方法。它需要三个参数：scope 表示当前堆栈，id 表示此构造函数的唯一 ID，
    # downstream 是一个 AWS Lambda 函数，它需要被计算其调用次数。
    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        # 调用父类 Construct 的构造函数来创建此自定义构造函数的实例。
        super().__init__(scope, id, **kwargs)

        # 通过 Table 类的构造函数创建了一个名为 table 的 DynamoDB 表对象
        self._table = ddb.Table(
            # self：表示当前类实例对象自身，即在当前栈中创建的 DynamoDB 表所属的栈。
            # 'Hits'：表示 DynamoDB 表的名称。
            self, 'Hits',
            # partition_key：一个字典，表示 DynamoDB 表的分区键。其中，'name' 表示分区键的名称，'type' 表示分区键的数据类型，此处为字符串类型。
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING},
            # removal_policy：表示表的删除策略，此处为移除所有表的数据。
            # RemovalPolicy.DESTROY：表示表的删除策略，此处为移除所有表的数据。
            removal_policy=RemovalPolicy.DESTROY,
        )
        
        #  创建一个名为 _handler 的 Lambda 函数，将其保存到 self._handler 变量中。
        self._handler = _lambda.Function(
            # 在当前堆栈下创建一个名为 HitCountHandler 的 Lambda 函数。
            self,
            'HitCountHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            # 将 Lambda 函数的代码从 asset 目录中加载。
            code=_lambda.Code.from_asset('lambda'),
            # 设置 Lambda 函数的处理程序为 hitcount.handler。
            handler='hitcount.handler',
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                'HITS_TABLE_NAME': self._table.table_name,
            }
        )

        # is not authorized to perform: dynamodb:UpdateItem on resource:
        self._table.grant_read_write_data(self._handler)
        # is not authorized to perform: lambda:InvokeFunction on resource: 
        downstream.grant_invoke(self._handler)
```
Write lambda/hitcount.py for the Lambda above
```python
import json
import os

import boto3

# 创建 DynamoDB 和 Lambda 的客户端资源对象
ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['HITS_TABLE_NAME'])
_lambda = boto3.client('lambda')

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    
    # 更新 DynamoDB 表中的记录
    table.update_item(
        # Key 参数指定要更新的记录的主键；
        Key={'path': event['path']},
        # 将 hits 字段值加上一个 :incr 参数的值
        UpdateExpression='ADD hits :incr',
        # 指定了 :incr 参数的实际值为 1
        ExpressionAttributeValues={':incr': 1}
    )
    
    # 调用另一个 Lambda 函数处理请求
    resp = _lambda.invoke(
        FunctionName=os.environ['DOWNSTREAM_FUNCTION_NAME'],
        Payload=json.dumps(event),
    )
    
    # 获取返回结果并打印
    body = resp['Payload'].read()
    print('downstream response: {}'.format(body))
    # 返回响应结果
    return json.loads(body)
```

## Troubleshooting with Cloudwatch Logs

## Use 3rd party module to view DynamoDb table

pip install cdk-dynamo-table-view==0.2.0

```python
from cdk_dynamo_table_view import TableViewer

        TableViewer(
            self, 'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table,
        )
```
Todo: Learn how this module was built
