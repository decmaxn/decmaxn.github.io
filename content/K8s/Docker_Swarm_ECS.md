---
title: "Docker_Swarm_ECS"
date: 2023-03-14T21:32:18-04:00
draft: false
tags: ["AWS","Docker","Tips"]
---

# Creat an example app with docker swarm

Here is an app based on latest wordpress and mysql 5.7 docker image.
```bash
$ cat <<EOF > stack.yaml
version: '3.1'

services:
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: example
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress

  wordpress:
    image: wordpress:latest
    ports:
      - "8000:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
EOF
$ docker swarm init
$ docker stack deploy -c stack.yaml mywordpress

Creating network mywordpress_default
Creating service mywordpress_wordpress
Creating service mywordpress_db

$ docker stack rm mywordpress 
```
To test it, browse http://127.0.0.1:8000 to see the workpress new user page.

# Creat the same app on ECS

## Install ECS CLI

```bash
sudo curl -Lo /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
vi ecs_cli_gpg.txt # copy/paste Amazon ECS PGP public key
gpg --import ecs_cli_gpg.txt
curl -Lo ecs-cli.asc https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest.asc
gpg --verify ecs-cli.asc /usr/local/bin/ecs-cli
sudo chmod +x /usr/local/bin/ecs-cli
```
## Configuring ECS CLI
Configuration information is stored in the ~/.ecs directory on macOS and Linux systems 

```bash
$ ecs-cli configure profile \
    --access-key $AWS_ACCESS_KEY_ID \
    --secret-key $AWS_SECRET_ACCESS_KEY
    # --profile-name dec
$ cat ~/.ecs/credentials # created by above configure profile --profile-name dec command
version: v1
default: default
ecs_profiles:
  default:
    aws_access_key_id: <AWS_ACCESS_KEY_ID>
    aws_secret_access_key: <AWS_SECRET_ACCESS_KEY>
$ ecs-cli configure \
    --cluster test-fargate-App \
    --region us-east-1 \
    --default-launch-type FARGATE
    # --config-name dec
$ cat ~/.ecs/config # this file is created by above ecs-cli configure command
version: v1
default: default
clusters:
  default:
    cluster: test-fargate-App
    region: us-east-1
    default_launch_type: FARGATE
```
## Creat ECS Cluster

This command "surprisingly" created a Cloudformation stack "amazon-ecs-cli-setup-test-fargate-App".

All this CF template deployed is a VPC, however the ECS cluster is created outside of this CF template. I believe if the default_launch_type is not FARGATE, the EC2 instances will be created since I do see them in the CF template with conditions.

```bash
$ ecs-cli up
    # --cluster-config dec \
    # --ecs-profile dec
```

## Create task definiation
Following [ecs-cli official repo](https://github.com/aws/amazon-ecs-cli#creating-an-ecs-cluster) to create 2 files.
```bash
$ cat <<EOF > docker-compose.yml
version: '3'
services:
    mysql:
        image: mysql:5.7
        environment:
            MYSQL_ROOT_PASSWORD:
    wordpress:
        image: wordpress
        ports:
            - "80:80"
EOF
$ cat <<EOF > ecs-params.yml
version: 1
task_definition:
  ecs_network_mode: awsvpc
  task_size:
    mem_limit: 2GB
    cpu_limit: 512
run_params:
  network_configuration:
    awsvpc_configuration:
      subnets:
        - "subnet-0f8e36255ab1ac868"
        - "subnet-0a38fe5a081e8eead"
      assign_public_ip: ENABLED         
EOF
$ 
```
Todo: using the following commands I should be able to create tasks and service. 
```bash
$ ecs-cli compose --project-name wordpress-test service create
$ ecs-cli compose --project-name wordpress-test service ps
```