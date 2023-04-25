---
title: "Swap_ecs_task_in_service"
date: 2023-02-15T08:50:56-05:00
draft: false
tags: ["coding","python","boto3","Aws"]
---

# Start another ECS task for service before stop the original task

I have made an improvement to my [stop ecs task ](../stop_ecs_task)Lambda function that manages my ECS service in a more graceful manner. Previously, it would stop the task associated with my ECS service to trigger a service refresh. This would result in the service being offline for a few minutes.

With this improvement, it now increases the task count to 2, effectively launching a new task. This new task runs in parallel with the existing task, ensuring that there is no downtime for my ECS service. Once the new task is confirmed as stable, it then proceeds to stop the old task.

By doing this, my ECS service remains available throughout the entire update process, as the new task is already running and handling requests before the old task is stopped. This ensures a smooth and uninterrupted user experience, as my service is always available.

```python
import boto3 
import os
import time

# The handler function is triggered when the AWS Lambda function is executed.
def handler(event, context):
    # This app change desired number to 2 and wait for it stable, then change it back after kill old runing tasks

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

    # A helper function to use 'list_tasks' method of the ECS client is called to retrieve a list of all running tasks for the specified service in the cluster.
    def listtasks():
        response = client.list_tasks(
            cluster=cluster_name,
            desiredStatus='RUNNING',
            serviceName=service_name,
            launchType='FARGATE'
        )
        tasks = response["taskArns"]
        print(f"Running tasks: {tasks}")
        return tasks

    # A helper function to change the desired number 
    def desiredcount(new_desired_count):
        response = client.update_service(
            cluster=cluster_name,
            service=service_name,
            desiredCount=new_desired_count
        )
        print(f"Updated Service {service_name} to have {new_desired_count} desired numbers")

    # A helper function to Wait for service to be stable
    def wait_service_stable():
        max_attempts = 36 # set a maximum number of attempts to prevent an infinite loop
        attempts = 0
        while True:
            describe_response = client.describe_services(
                cluster=cluster_name,
                services=[service_name]
            )
            service = describe_response['services'][0]
            running_count = service['runningCount']
            desired_count = service['desiredCount']
            # print(f"Running tasks: {running_count}/{desired_count}")
            if running_count == desired_count:
                print(f"Service {service_name} now has {running_count} running tasks")
                break
            attempts += 1
            if attempts >= max_attempts:
                print(f"Service {service_name} did not become stable within {max_attempts} attempts")
                break
            time.sleep(10)

    # Increase desired number to 2 and wait for it become stable
    tasks = listtasks() 
    desiredcount(2)
    wait_service_stable()

    # A for loop iterates over the task IDs and calls the stoptask function, passing in the task ID and a reason for stopping the task. The response from the stoptask function is printed.
    for task in tasks:
        stoptask(task,"Daily refresh")
        print(f"Stopped the originally running task {task}")

    # Decrease desired number back to 1 and wait for it become stable
    desiredcount(1)
    wait_service_stable()
    listtasks()
```

functions stoptask, listtasks, desiredcount and wait_service_stable have all been used more than once.