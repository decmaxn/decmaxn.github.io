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