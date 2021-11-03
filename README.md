# Serverless Flask Sample

Simple fully managed API server using API Gateway, Lambda, DynamoDB, and Flask. And deploy the infrastructure by [serverless framework](https://serverless.com/).
# Deploy Lambda Function and API Gateway using
![image](https://user-images.githubusercontent.com/28998255/140038981-535b348f-3b43-48f9-ae9f-a342085cd87b.png)


AWS lambda is a service that lets the user to run code without provisioning or managing servers and the user needs to pay for how much they use. The user can also scale it up and down according to their needs. Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently. It uses Infrastructure as Code to provision and manage any cloud, infrastructure, or service.
AWS API gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor and secure APIs. API acts as a front door for the application to access data, business logic or functionality from the backend services. It handles all the task involved in accepting and processing up of hundreds or thousands of concurrent API calls, including traffic management, authorization, access control, monitoring and API management.


# In this walk-through, we will:

Deploy a simple API endpoint
Add a DynamoDB table and two endpoints to create and retrieve a User object
Set up path-specific routing for more granular metrics and monitoring
Configure your environment for local development for a faster development experience.

# Getting Started
To get started, you'll need the Serverless Framework installed. 
You'll also need your environment configured with AWS credentials.
Getting Started
To get started, you'll need the Serverless Framework installed. You'll also need your environment configured with AWS credentials.

Creating and deploying a single endpoint
Let's start by deploying a single endpoint.

# First, create a new directory with a package.json file:
```
$ mkdir my-flask-application && cd my-flask-application
$ npm init -f
Copy
Then, install a few dependencies. We're going to use the serverless-wsgi plugin for negotiating the API Gateway event type into the WSGI format that Flask expects. We'll also use the serverless-python-requirements plugin for handling our Python packages on deployment.

$ npm install --save-dev serverless-wsgi serverless-python-requirements
Copy
```
With our libraries installed, let's write our Flask application. Create a file app.py with the following contents:

main.py

```
import os
from flask import Flask, request, jsonify, abort
import boto3
from datetime import date

app = Flask(__name__)


TODOS_TABLE = os.environ['TODOS_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TODOS_TABLE)




def get_todo(username):
    res = table.get_item(Key={ 'username': username })
    year, month, day = res["date_of_birth"].split("-")
    today = date.today()
    if today.month == int(month) and today.day == int(day):
       return jsonify({"message": f"Hello, {username}! Happy birthday!"})

    else:
        month_diff = today.month - int(month)
        day_diff = today.day - int(day)
        return jsonify({"message": f"Hello, {username}! Your birthday is in {(12 + month_diff) * 30 + day_diff} day(s)"})



def new_id():
    res = table.scan()
    ary = res['Items']
    if len(ary) == 0:
        return '1'
    else:
        ary = sorted(ary, key=lambda x: x['username'], reverse=True)
        return str(int(ary[0]['username']) + 1)



@app.route("/hello/<username>")
def show(username):
    todo = get_todo(username)
    return jsonify(todo),


@app.route("/hello/<username>", methods=["PUT"])
def update(username):
    date_of_birth = request.json.get('date_of_birth')
    if not date_of_birth:
        return jsonify({'error': 'Please provider todo  date_of_birth'}), 422
    new_todo = { 'username': new_id(), 'date_of_birth': date_of_birth }
    res = table.put_item(Item=new_todo)

     return jsonify(new_todo), 201

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

```
To get this application deployed, create a serverless.yml in the working directory:


# Adding a DynamoDB table with REST-like endpoints
Doing a "Hello World!" is fun, but your application will need to persist some sort of state to be useful. Let's add a DynamoDB table.
 We want to store them by username, which is a unique identifier for a particular user.

First, we'll need to configure our serverless.yml to provision the table. This involves three parts:


Provisioning the table in the resources section;
Adding the proper IAM permissions; and Passing the table name as an environment variable so our functions can use it.
Change your serverless.yml to look as follows:

```
# serverless.yml

service: serverless-flask-sample

plugins:
  - serverless-python-requirements
  - serverless-wsgi

custom:
  tableName: 'todos-${self:provider.stage}'
  wsgi:
    app: main.app
    packRequirements: false

provider:
  name: aws
  runtime: python3.6
  stage: dev
  region: ap-northeast-1
  iamRoleStatements:
    - Effect: Allow
      Action:
        - dynamodb:Query
        - dynamodb:Scan
        - dynamodb:GetItem
        - dynamodb:PutItem
        - dynamodb:UpdateItem
        - dynamodb:DeleteItem
      Resource:
        - { "Fn::GetAtt": ["TodosDynamoDBTable", "Arn" ] }
  environment:
    TODOS_TABLE: ${self:custom.tableName}

functions:
  app:
    handler: wsgi.handler
    events:
      - http: ANY /
      - http: 'ANY {proxy+}'

resources:
  Resources:
    TodosDynamoDBTable:
      Type: 'AWS::DynamoDB::Table'
      DeletionPolicy: Retain
      Properties:
        TableName: ${self:custom.tableName}
        AttributeDefinitions:
          -
            AttributeName:  username
            AttributeType: S
        KeySchema:
          -
            AttributeName: username
            KeyType: HASH
        ProvisionedThroughput:
          ReadCapacityUnits: 5
          WriteCapacityUnits: 5
```

The handler is handler function from the wsgi module. Note that this module will be added to our deployment package by the serverless-wsgi plugin 

# Tools & Packages

* [Amazon API Gateway](https://aws.amazon.com/api-gateway/)
* [AWS Lambda](https://aws.amazon.com/lambda/)
* [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
* [serverless](https://serverless.com/) 1.27.3 (npm package)
* [serverless-wsgi](https://github.com/logandk/serverless-wsgi) 1.4.8
* [serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements) 4.1.0
* [Flask](http://flask.pocoo.org/) 1.0.2 (API server)
* Python 3.6.1 (by pyenv)
* aws-cli 1.15.45 (by pyenv)
* node v10.5.0 (by ndenv)

## Prerequisite

* node.js (npm) greater than or equal to v4
* aws account
* awscli

## Setup & Deploy

```
# Download source
git clone git@github.com:esmaeilzadehayub/AWS-SERVERLESS.git
cd serverless-flask-sample

# Install serverless globally
npm install serverless -g

# Deploy to aws
serverless deploy -v

# Remove deplyed resources
serverless remove
```

## Samples

```
export SLS_ENDPOINT=https://m56ha23xqf.execute-api.ap-northeast-1.amazonaws.com/dev

# get a hello/test
curl ${SLS_ENDPOINT}/hello/<username>
> {"error":"Not found"}

# PUT a hello/test
curl ${SLS_ENDPOINT}/hello/test -X POST -H "Content-Type: application/json" -d '{"date_of_birth": "1988-01-02"}'
> {"username":"test","date_of_birth":"1988-01-02"}

# get a hello/test again
curl ${SLS_ENDPOINT}/hello/<username>
> {"username":"test","date_of_birth":"1988-01-02"}


```
