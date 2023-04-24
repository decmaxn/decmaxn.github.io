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
