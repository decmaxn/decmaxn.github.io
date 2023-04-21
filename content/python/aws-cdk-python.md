---
title: "Aws Cdk with Python"
date: 2023-04-06T20:08:29-04:00
draft: false
tags: ["python", "AWS", "tips", "CDK"]
---

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