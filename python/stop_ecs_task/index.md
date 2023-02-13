# Stop_ecs_task


# Interact with AWS resource with boto3

This is used in an AWS Lambda been triggered daily to do a maintenance task.

Todo: Add logging

```python
import boto3 
import os
def handler(event, context):
    " This function stop all AWS ECS tasks of CLUSTER_NAME and SERVICE_NAME when it's triggered

    client = boto3.client('ecs')
    
    cluster_name = os.environ['CLUSTER_NAME']
    service_name = os.environ['SERVICE_NAME']
    
    def stoptask(task_id, reason):
        
        resp = client.stop_task(
            cluster=cluster_name,
            task=task_id,
            reason= "Daily refresh" 
            )
        return resp

    response = client.list_tasks(
    cluster=cluster_name,
    desiredStatus='RUNNING',
    serviceName=service_name,
    launchType='FARGATE'
    )

    tasks = response["taskArns"]
    
    for task in tasks:
        resp = stoptask(task,"testing_lambda")
        print(resp)
```
