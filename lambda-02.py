import json
import boto3

sns = boto3.client('sns')
ses = boto3.client('ses')  # Make sure you're using the correct SES region

# Replace with your actual SES verified email address
sender_email = 'edwin.benny@techconsulting.tech'

def lambda_handler(event, context):
    for record in event['Records']:
        sns_message = json.loads(record['Sns']['Message'])
        email = sns_message['email']
        otp = sns_message['otp']
        
        subject = 'Your OTP Code'
        body = f'Your OTP code is {otp}. It is valid for 5 minutes.'
        
        try:
            response = ses.send_email(
                Source=sender_email,
                Destination={
                    'ToAddresses': [email]
                },
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': body}}
                }
            )
            
            return {
                'statusCode': 200,
                'body': json.dumps({'success': True, 'message': 'Email sent successfully.'})
            }
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({'success': False, 'message': 'Error sending email.'})
            }
