# Serverless Flask Sample

Simple fully managed API server using API Gateway, Lambda, DynamoDB and Flask. And deploy the infrastructure by [serverless framework](https://serverless.com/).

## Tools & Packages

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

# get all hello/<username> list
curl ${SLS_ENDPOINT}/hello/<username>
> [ ]

# get a hello/<username>
curl ${SLS_ENDPOINT}/hello/<username>
> {"error":"Not found"}

# PUT a hello/<username>
curl ${SLS_ENDPOINT}/hello/test -X POST -H "Content-Type: application/json" -d '{"date_of_birth": "1988-01-02"}'
> {"username":"test","date_of_birth":"1988-01-02"}

# get a hello/<username> again
curl ${SLS_ENDPOINT}/hello/<username>
> {"username":"test","date_of_birth":"1988-01-02"}


```
