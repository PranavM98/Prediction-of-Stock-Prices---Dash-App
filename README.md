# Real Time Stock Prediction Dash Application

Introduction
<img width="1792" alt="Screen Shot 2020-11-24 at 5 27 46 AM" src="https://user-images.githubusercontent.com/30974949/100028858-d5238d80-2e15-11eb-8c30-efa063e22b09.png">
<align="center">Application Front Page
Welcome to the Real Time Stock Prediction Application. The main objective of this project is to predict the next minute of Amazon Stock Price based on the current stock price and the previous 150 observation. This project is extremely useful for those actively selling and buying stocks in a day.

As shown in the Figure above, the application consists of 2 buttons. The "Refresh" button will automatically restart the application and extract the most current stock price from the S3 bucket. The "Predict" button will then run the prediction algorithm (SARIMAX Time Series Forecasting) and display the predictions on the Application.


Cloud Diagram



Cloud Services Used:
2. AWS S3
4. AWS Lambda
5. AWS DynamoDB
6. AWS CloudWatch

Technologies Used:
1. Dash Plotly Application - Python
2. CSS Styling
3. Github
4. Docker and DockerHub


This project is broken down into 3 phases.

Phase 1
1) This phase consists of using Amazon DynamoDB, Amazon S3, Amazon CloudWatch and two Amazon Lambda functions.
The first lambda function is triggered by a CloudWatch event which executes the function every minute from 9:30 am to 4 pm Monday - Friday (When the stock market is open). The lambda function scapes marketinsider.com for the stock price of Amazon, NASDAQ, S&P 50, and DowJones and stores this data in a DynamoDB table.

The second lambda function is triggered by a DynamoDB event and is executed when there is an addition/reduction of data in/from the DynamoDB table. This lambda function fetches the data from DynamoDB and stores it in a S3 Bucket as a JSON format.

As both lambda functions are interconnected, new data will be updated every minute and stored into the DynamoDB as well as the S3 bucket.

Phase 2
This phase consists of deploying the Dash Application on AWS Elastic Beanstalk. The application implements Continuous Deployment and Continuous Integration (CD / CI) with AWS Code Build and Github.



How to Run the App
