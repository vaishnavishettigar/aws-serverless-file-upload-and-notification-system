Add WeeklyUploadSummaryLambda function

import boto3
from datetime import datetime, timedelta
# AWS clients
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
# DynamoDB tables
UPLOAD_TABLE = dynamodb.Table('FileUploadEvents')
ERROR_TABLE = dynamodb.Table('UploadErrors')
# SNS Topic ARN (weekly summary)
SUMMARY_TOPIC_ARN = "arn:aws:sns:us-east-1:686354459805:weekly-upload-summary-topic-v2"
def lambda_handler(event, context):
# Current time and 7-day window (UTC, naive – SAFE)
now = datetime.utcnow()
seven_days_ago = now - timedelta(days=7)
# ---------------------------
# Read upload records
# ---------------------------
upload_items = UPLOAD_TABLE.scan().get('Items', [])
total_files = 0
total_size = 0
file_type_count = {}
for item in upload_items:
# SAFE timestamp parsing (no timezone errors)
upload_time = datetime.strptime(
item['uploadTime'][:19], "%Y-%m-%dT%H:%M:%S"
)
if upload_time >= seven_days_ago:
total_files += 1
total_size += int(item.get('fileSize', 0))
ftype = item.get('fileType', 'Unknown')
file_type_count[ftype] = file_type_count.get(ftype, 0) + 1
# ---------------------------
# Read error records
# ---------------------------
error_items = ERROR_TABLE.scan().get('Items', [])
recent_errors = []
13
for err in error_items:
error_time = datetime.strptime(
err['errorTime'][:19], "%Y-%m-%dT%H:%M:%S"
)
if error_time >= seven_days_ago:
recent_errors.append(err.get('errorMessage', 'Unknown error'))
# ---------------------------
# Build email content
# ---------------------------
message = f"""
7-Day Upload Summary Report
Time Period:
{seven_days_ago.date()} to {now.date()}
Total Files Uploaded: {total_files}
Total Upload Size: {total_size} bytes
File Type Breakdown:
"""
if file_type_count:
for ftype, count in file_type_count.items():
message += f"- {ftype}: {count} files\n"
else:
message += "- No files uploaded\n"
message += "\nErrors Detected:\n"
if recent_errors:
for e in recent_errors:
message += f"- {e}\n"
else:
message += "None\n"
# ---------------------------
# Send email via SNS
# ---------------------------
sns.publish(
TopicArn=SUMMARY_TOPIC_ARN,
Subject="7-Day File Upload Summary",
Message=message
)
return {
"statusCode": 200,
"body": "7-day summary email sent successfully
