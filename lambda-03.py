import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('OtpTable')

def lambda_handler(event, context):
    try:
        print(f"Event received: {event}")

        body = event.get('body', {})
        if isinstance(body, str):
            body = json.loads(body)
        
        print(f"Parsed body: {body}")
        
        email = body.get('email')
        otp = body.get('otp')
    except KeyError as e:
        print(f"KeyError: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'success': False, 'message': 'Missing parameter: \'body\''})
        }

    if not email or not otp:
        print(f"Missing email or OTP: email={email}, otp={otp}")
        return {
            'statusCode': 400,
            'body': json.dumps({'success': False, 'message': 'Email or OTP missing'})
        }

    print(f"Received email: {email}")
    print(f"Received OTP: {otp}")

    try:
        response = table.get_item(
            Key={
                'email': email
            }
        )
        item = response.get('Item')

        print(f"DynamoDB get_item response: {response}")
        print(f"Item found: {item}")

        if not item:
            return {
                'statusCode': 400,
                'body': json.dumps({'success': False, 'message': 'No OTP found for this email'})
            }

        if item['otp'] != otp:
            print("OTP does not match.")
            return {
                'statusCode': 400,
                'body': json.dumps({'success': False, 'message': 'Invalid OTP'})
            }

        if item['status'] == 'used':
            print("OTP has already been used.")
            return {
                'statusCode': 400,
                'body': json.dumps({'success': False, 'message': 'OTP already used'})
            }

        # Mark OTP as used
        table.update_item(
            Key={'email': email},
            UpdateExpression="SET #s = :used",
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':used': 'used'}
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'success': True, 'message': 'OTP verified successfully'})
        }

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'success': False, 'message': str(e)})
        }
