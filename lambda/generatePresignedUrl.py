import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')

BUCKET_NAME = "vaishnavi-upload-bucket"

def lambda_handler(event, context):
    body = json.loads(event['body'])

    file_name = body['fileName']
    file_type = body['fileType']

    key = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_name}"

    presigned_url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': key,
            'ContentType': file_type
        },
        ExpiresIn=300
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': json.dumps({
            'uploadURL': presigned_url
        })
    }
