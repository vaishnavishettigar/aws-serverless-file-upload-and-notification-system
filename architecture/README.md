This folder contains the architecture and workflow diagrams of the AWS Serverless File Upload and Notification System.

Workflow:
User → API Gateway → Lambda → S3 → SNS → DynamoDB → EventBridge → Weekly Summary Lambda → Email Notification
