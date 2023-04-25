---
title: "Stop_ecs_task"
date: 2023-02-13T08:43:10-05:00
draft: false
tags: ["coding","python","boto3","Aws"]
---

# Interact with AWS resource with boto3

This is used in an AWS Lambda been triggered daily to do a maintenance task.
The infrastructure part is done by SAM. 

```python
import boto3 
import os

# The handler function is triggered when the AWS Lambda function is executed.
def handler(event, context):
    # This app stops all running tasks of an ECS cluster and service.

    # The boto3 library is imported and the 'ecs' client is created using boto3.client().
    client = boto3.client('ecs')
    
    # The cluster_name and service_name are read from environment variables 'CLUSTER_NAME' and 'SERVICE_NAME'.
    cluster_name = os.environ['CLUSTER_NAME']
    service_name = os.environ['SERVICE_NAME']
    print(f"Cluster name: {cluster_name}")
    print(f"Service name: {service_name}")

    # A helper function "stoptask" is defined that takes in a task ID and a reason for stopping the task.
    def stoptask(task_id, reason):
        
        # This function stops the task by calling the 'stop_task' method of the ECS client, passing the cluster_name, task ID, and reason for stopping the task.
        resp = client.stop_task(
            cluster=cluster_name,
            task=task_id,
            reason= "Daily refresh" 
            )
        print(f"Task ID: {task_id}")
        print(f"Response from stop_task: {resp}")
        return resp

    # The 'list_tasks' method of the ECS client is called to retrieve a list of all running tasks for the specified service in the cluster.
    response = client.list_tasks(
        cluster=cluster_name,
        desiredStatus='RUNNING',
        serviceName=service_name,
        launchType='FARGATE'
    )

    tasks = response["taskArns"]
    print(f"Running tasks: {tasks}")

    # A for loop iterates over the task IDs and calls the stoptask function, passing in the task ID and a reason for stopping the task. The response from the stoptask function is printed.
    for task in tasks:
        resp = stoptask(task,"Daily refresh")
        print(f"Stopping task: {resp}")
```