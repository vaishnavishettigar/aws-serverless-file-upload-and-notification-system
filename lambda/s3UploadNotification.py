Add S3 upload notification Lambda

import json
import boto3
from datetime import datetime

# AWS clients
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

# DynamoDB table
TABLE_NAME = "FileUploadEvents"
table = dynamodb.Table(TABLE_NAME)

# SNS Topic ARNs
FILE_TOPIC_ARN = "arn:aws:sns:us-east-1:686354459805:file-upload-topic"
IMAGE_TOPIC_ARN = "arn:aws:sns:us-east-1:686354459805:image-upload-topic"
PDF_TOPIC_ARN = "arn:aws:sns:us-east-1:686354459805:pdf-upload-topic"


def lambda_handler(event, context):
    try:
        # Get S3 event details
        record = event['Records'][0]

        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        file_size = record['s3']['object']['size']

        upload_time = datetime.utcnow().isoformat()

        file_name = object_key.split('/')[-1]
        file_extension = file_name.split('.')[-1].lower()

        # Determine file type and SNS topic
        if file_extension in ['jpg', 'jpeg', 'png']:
            topic_arn = IMAGE_TOPIC_ARN
            file_type = "Image"

        elif file_extension == 'pdf':
            topic_arn = PDF_TOPIC_ARN
            file_type = "PDF"

        else:
            topic_arn = FILE_TOPIC_ARN
            file_type = "Other"

        # Store metadata in DynamoDB
        table.put_item(
            Item={
                "fileName": file_name,
                "uploadTime": upload_time,
                "fileSize": file_size,
                "fileType": file_type,
                "bucketName": bucket_name
            }
        )

        # Build notification message
        message = f"""
New file uploaded successfully!

File Name: {file_name}
File Type: {file_type}
File Size: {file_size} bytes
Bucket: {bucket_name}
Upload Time: {upload_time}
"""

        # Send SNS notification
        sns.publish(
            TopicArn=topic_arn,
            Subject="New File Upload Notification",
            Message=message
        )

        return {
            "statusCode": 200,
            "body": json.dumps("Metadata stored and notification sent")
        }

    except Exception as e:
        print("ERROR:", str(e))
        raise e
