# AWS Serverless File Upload and Notification System

## Project Overview

This project is a serverless file upload system built using AWS services. Users upload files through a web interface, files are stored in Amazon S3, notifications are sent using Amazon SNS, metadata is stored in DynamoDB, and weekly upload summaries are generated automatically using EventBridge and AWS Lambda.

## AWS Services Used

- Amazon S3
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon SNS
- Amazon EventBridge
- Amazon CloudWatch
- AWS IAM

## Architecture

See the architecture folder for workflow diagrams.

## Features

- Secure file uploads using pre-signed URLs
- Automatic file upload notifications
- Metadata storage in DynamoDB
- Weekly upload summary emails
- Fully serverless architecture

## Screenshots

- S3 Buckets
- API Gateway
- Lambda Functions
- DynamoDB Tables
- Architecture Diagram

## Project Structure

frontend/ - Web application files

lambda/ - Lambda function source code

architecture/ - Architecture diagrams

screenshots/ - AWS resource screenshots

## Author

Vaishnavi Shettigar
