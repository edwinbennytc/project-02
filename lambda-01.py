import json
import boto3
import random
import string
import time

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
table = dynamodb.Table('OtpTable')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body.get('email')
    
    if not email or not validate_email(email):
        return {
            'statusCode': 400,
            'body': json.dumps({'success': False, 'message': 'Invalid email address.'})
        }
    
    otp = ''.join(random.choices(string.digits, k=6))
    expiration_time = int(time.time()) + 5 * 60  # 5 minutes expiration
    
    table.put_item(
        Item={
            'email': email,
            'otp': otp,
            'expiration_time': expiration_time,
            'status': 'unused'
        }
    )
    
    message = {
        'email': email,
        'otp': otp
    }
    
    sns.publish(
        TopicArn='arn:aws:sns:ap-southeast-2:866934333672:OtpNotificationTopic',
        Message=json.dumps(message)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'success': True, 'message': 'OTP generated and sent successfully.'})
    }

def validate_email(email):
    import re
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
