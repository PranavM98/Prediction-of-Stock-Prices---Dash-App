# Real Time Amazon Stock Prediction Dash Application - AWS 

## Introduction
![Stock Prediction Dash Application](https://user-images.githubusercontent.com/30974949/100032921-15d3d480-2e1f-11eb-8eaa-5d5fdd3f23ad.png)



Welcome to the Real Time Stock Prediction Application. The main objective of this project is to predict the next minute of Amazon Stock Price based on the current stock price and the previous 150 observations. This project is useful for those actively selling and buying stocks in a day.

As shown in the Figure above, the application consists of 2 buttons. The "Refresh" button will automatically restart the application and extract the most current stock price from the S3 bucket. The "Predict" button will then run the prediction algorithm (SARIMAX Time Series Forecasting) and display the predictions on the Application.

### This github repo also uses Github Actions for Continuous Integration as shown in the image below. 

<img width="1792" alt="Screen Shot 2020-11-24 at 1 17 55 PM" src="https://user-images.githubusercontent.com/30974949/100063737-a6c6a200-2e57-11eb-8355-151d5ea3524c.png">

## Cloud Diagram

<img width="1792" alt="Screen Shot 2020-11-24 at 5 31 47 AM" src="https://user-images.githubusercontent.com/30974949/100029065-63980f00-2e16-11eb-9f62-0ffa0160f664.png">


AWS Cloud Services Used:
1. AWS S3
2. AWS Lambda
3. AWS DynamoDB
4. AWS CloudWatch

Technologies Used:
1. Dash Plotly Application - Python
2. CSS Styling
3. Github
4. Docker and DockerHub


This project is broken down into 2 phases.

### Phase 1 (Orange Box in Cloud Diagram)

This phase consists of using Amazon DynamoDB, Amazon S3, Amazon CloudWatch and two Amazon Lambda functions.
The first lambda function (AWS Lambda Function 1) is triggered by a CloudWatch event which executes the function every minute from 9:30 am to 4 pm Monday - Friday (When the stock market is open). The lambda function scapes marketinsider.com for the stock price of Amazon, NASDAQ, S&P 50, & DowJones, formats the data into a Pandas DataFrame, and stores this data in a DynamoDB table.

The second lambda function (AWS Lambda Function 2) is triggered by a DynamoDB event and is executed when there is an addition/reduction of data in/from the DynamoDB table. This lambda function fetches the data from DynamoDB and stores it in a S3 Bucket as a JSON format.

As both lambda functions are interconnected, new data will be updated every minute and stored into the DynamoDB as well as the S3 bucket.

#### AWS Lambda Function 1:

```python

import json
import cli
import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import boto3
import time
import csv
import test
import prediction
import scrape
import analysis

dynamodb=boto3.resource('dynamodb')
dynamoTable=dynamodb.Table('stocks_tables')


def lambda_handler(event, context):
    
    #cli.py contains a function named start1 which scrapes the web and returns a single row dataframe with the stock prices at that time.
    df=cli.start1()
    
    #Storing data into local variables
    time_str=str(df.iloc[-1,4])
    stock_price=str(df.iloc[-1,5])
    company=str(df.iloc[-1,3])
    sp=str(df.iloc[-1,0])
    nd=str(df.iloc[-1,1])
    dj=str(df.iloc[-1,2])
    

    #Appending the data into the DynamoDB table.
    dynamoTable.put_item(
        Item={
        'Date_Time': time_str,
        'Company':company,
        'Stock Price':stock_price,
        'S&P 50': sp,
        'Nasdaq': nd,
        'DowJones': dj
        }
        )
    
    #Used for logging. Not required
    return {
        'statusCode': 200,
        'Date_Time': time_str,
        'Company':company,
        'Stock Price':stock_price,
        'S&P 50': sp,
        'Nasdaq': nd,
        'DowJones': dj
    }



```
#### AWS Lambda Function 2:

```python

import json
import boto3
import os

# Initializing the Services used

s3=boto3.client('s3')
ddb=boto3.resource('dynamodb')
table=ddb.Table('stocks_tables')

def lambda_handler(event, context):


    #Scans the DynamoDB table
    response=table.scan()
    
    #Body contains the table values/data
    body=json.dumps(response['Items'])
    
    #s3.put_Object places the DynamoDB data into the s3 bucket
    response=s3.put_object(Bucket='stocks-dump', Key='stocks-dump.json', Body=body,
    ContentType='application/json')
    
    
```


### Phase 2 (Blue box in Cloud Diagram)

This phase consists of creating a Dash Application, storing the application in a Docker Image, and uploading the image to DockerHub. Below is a screenshot of the application after pressing the "Predict" Button.

<img width="1792" alt="Screen Shot 2020-11-24 at 5 53 39 AM" src="https://user-images.githubusercontent.com/30974949/100030403-6ea06e80-2e19-11eb-9cb9-b7004597126e.png">


As shown in the image above, the current price is $3100.18 (Inside Yellow Box). The model predicted that the next minute's Amazon stock price is $3099.48 (A decrease of $0.7 when compared to the current price)

Creating the Docker Image:
```
docker build --tag dashapp .
```

Pushing the Docker Image to DockerHub
```
docker login --username=pranavm98
docker image ls
docker tag <Image ID> pranavm98/dashapp:<tag name>
docker push pranavm98/dashapp
```


Key Points to Note: 1) As the application accesses the s3 bucket on my AWS account, in order to run the program, the user must have my AWS login credentials. 2) The port used throughout this project is 8080. 3) If using AWS Cloud9, edit the inbound rules to include port 8080.


How to Run the App

From DockerHub:

1) Pull Docker Image from DockerHub
```
docker pull pranavm98/dashapp:final
```
2) Run the DockerImage
```
docker run -rm -e AWS_ACCESS_KEY_ID=************* -e AWS_SECRET_ACCESS_KEY=***************** -e DEFAULT_REGION_NAME=us-east-2 -p 8080:8080  pranavm98/dashapp:final
```
3) Open the URL!

From Github:

1) Clone the repo
```
git clone https://github.com/PranavM98/Stock-Dash.git
```
2) Install the required packages
```
make install
```
3) Enable AWS configurations
```
aws configure
```
4) Run the application
```
python application.py
```
