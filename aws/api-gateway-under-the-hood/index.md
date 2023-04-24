# Api Gateway Under the Hood


## 底层设施
AWS API Gateway使用了多个分布式系统组件来提供其服务。这些组件包括 Amazon CloudFront、Amazon Route 53、AWS Elastic Load Balancing、AWS Lambda 等等。

当您创建一个 API Gateway 时，API Gateway 会在后台自动创建一个或多个 Amazon API Gateway REST API，并为每个 REST API 创建一个 Amazon CloudFront 分发。每个分发都有一个唯一的 DNS 名称，它充当 API 的公共入口点。

当客户端发送请求到 API Gateway 时，请求将被路由到正确的 Amazon CloudFront 分发。然后，Amazon CloudFront 将请求转发到与该 REST API 关联的 AWS Elastic Load Balancing 负载均衡器。负载均衡器将请求路由到一个或多个后端服务（如 AWS Lambda 函数或 EC2 实例）。

## 设计构架

### RestApi

在整个 API Gateway 中，AWS::ApiGateway::RestApi 位于 API Gateway 的顶层，它表示整个 API 的定义和配置。
```yaml
  Endpoint:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: Endpoint
```
这里仅仅是定义了 REST API 的名称，还没有定义 API 的具体资源和方法，因为它们需要使用 AWS::ApiGateway::Resource 和 AWS::ApiGateway::Method 资源类型进行定义。在定义了资源和方法之后，您需要使用 AWS::ApiGateway::Deployment 资源类型进行部署，才能将 API 置于生效状态。

### Resource
AWS::ApiGateway::Resource 是属于 AWS::ApiGateway::RestApi 的子资源类型，它表示一个特定的 API 资源 (请求路径)，例如 /users、/orders 等等。可以包含一个或多个子资源以及对应的方法。
```yaml
  Endpointproxy39E2174E:
    Type: AWS::ApiGateway::Resource
    Properties:
      # 父资源 ID，即 Endpoint REST API 的根资源 ID
      ParentId:
        # Fn::GetAtt: [ logicalNameOfResource, attributeName ]
        Fn::GetAtt:
        - Endpoint
        # The root resource ID for a RestApi resource, such as a0bc123d4e.
        - RootResourceId
      # 源的路径部分为 "{proxy+}"，它表示匹配任何请求路径
      # The last path segment for this resource.
      PathPart: "{proxy+}"
      # The string identifier of the associated RestApi.
      RestApiId:
        Ref: Endpoint
```
### Method
在 REST API 中，方法是资源的一部分，它定义了对资源的具体操作，例如 GET、POST、PUT 等等。每个方法都必须绑定到一个资源上，并且必须指定其对应的后端服务（例如 Lambda 函数或 EC2 实例）。
```yaml
  # 定义一个任意 HTTP 方法的 API 方法，并将其与 Endpointproxy39E2174E 资源相关联，并将请求路由到一个 AWS Lambda 函数
  EndpointproxyANYC09721C5:
    Type: AWS::ApiGateway::Method
    Properties:
      # 指定该方法的 HTTP 请求方法，例如 GET、POST、PUT 等等
      HttpMethod: ANY
      # 指定该方法所属的资源的 ID。
      ResourceId:
        Ref: Endpointproxy39E2174E
      # 指定该方法所属的 REST API 的 ID。
      RestApiId:
        Ref: Endpoint
      # 可选属性，指定该方法的授权类型，例如 NONE、AWS_IAM 等等
      AuthorizationType: NONE
      # 指定该方法与后端服务的集成方式，它定义了将请求路由到哪个后端服务上。
      Integration:
        # 使用 POST 方法将请求发送到后端 Lambda 函数。
        IntegrationHttpMethod: POST
        # AWS_PROXY 集成类型将通过 API Gateway 代理将所有 HTTP 请求传递给后端 Lambda 函数
        Type: AWS_PROXY
        # Lambda 函数的 ARN
        Uri:
          Fn::Join:
          - ''
          - - 'arn:'
            - Ref: AWS::Partition
            - ":apigateway:"
            - Ref: AWS::Region
            - ":lambda:path/2015-03-31/functions/"
            - Fn::GetAtt:
              - HelloHandler2E4FBA4D
              - Arn
            - "/invocations"
```
```yaml
  EndpointANY485C938B:
    Type: AWS::ApiGateway::Method
    Properties:
      HttpMethod: ANY
      ResourceId:
        Fn::GetAtt:
        - EndpointEEF1FD8F
        - RootResourceId
      RestApiId:
        Ref: EndpointEEF1FD8F
      AuthorizationType: NONE
      Integration:
        IntegrationHttpMethod: POST
        Type: AWS_PROXY
        Uri:
          Fn::Join:
          - ''
          - - 'arn:'
            - Ref: AWS::Partition
            - ":apigateway:"
            - Ref: AWS::Region
            - ":lambda:path/2015-03-31/functions/"
            - Fn::GetAtt:
              - HelloHandler2E4FBA4D
              - Arn
            - "/invocations"
```
### Deployment
 创建 AWS::ApiGateway::Deployment 资源，用于部署 REST API 的变更
```yaml
EndpointDeployment:
  Type: AWS::ApiGateway::Deployment
  Properties:
    # 指定要部署的 REST API 的 ID
    RestApiId:
      Ref: Endpoint
  # 指定此 Deployment 资源所依赖的其他资源，即 EndpointproxyANYC09721C5、Endpointproxy39E2174E、EndpointANY485C938B
  DependsOn:
  - EndpointproxyANYC09721C5
  - Endpointproxy39E2174E
  - EndpointANY485C938B
```
### Stage
用于指定 API Gateway 的部署版本（EndpointDeployment）所使用的阶段名称。
```yaml
  EndpointDeploymentStageprodB78BEEA0:
    Type: AWS::ApiGateway::Stage
    Properties:
      RestApiId:
        Ref: Endpoint
      # DeploymentId 指定该阶段使用的部署版本
      DeploymentId:
        Ref: EndpointDeployment
      StageName: prod
```

## 这里只有一个生产环境，测试环境呢？
要测试环境，需要创建另一个部署，指向不同的 API 网关阶段。可以通过修改 CloudFormation 模板，将新的部署和阶段添加到模板中。然后使用 CloudFormation 更新堆栈，以创建并部署新的测试环境。在这个新的测试环境中，您可以测试 API 的新版本，而不会影响生产环境的稳定性。
