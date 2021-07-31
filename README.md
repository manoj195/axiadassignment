# axiadassignment

This is the Python code using boto3 module for provisioning resources on AWS

Its using the combination of SDK and CloudFormation

Prereq:

1. Make sure AWS CLI, Python, pip3 and module boto3 are installed

2. Set the credentials file unser ~/.aws


Usage:

1. Clone the repo on your workspace

2. Trigger python3 awslcy.py

Code Flow:

1. Python code will create VPC, subnet, InternetGateway, Routetable

2. Python code using boto3 SDK will create Launch Configuration

3. Python code will trigger CLOUDFORMATION code which is creating the Auto scaling Group, RDS and ELB

4. CloudFormation code will be responsible for attaching the target group to ELB.

5. CloudFormation template is also attached as part of assignment
