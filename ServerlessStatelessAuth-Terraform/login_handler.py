import json
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table = dynamodb.Table('users-table')

cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST"
}

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        email = body['email']
        password = body['password']
        
        response = table.get_item(Key={'email': email})
        
        if 'Item' in response:
            db_user = response['Item']
            if db_user['password'] == password and db_user['is_logged_in'] == 'true':
                return {
                    "statusCode": 200,
                    "headers": cors_headers,
                    "body": json.dumps({"message": f"Welcome back, {email}!"})
                }
        
        return {
            "statusCode": 401,
            "headers": cors_headers,
            "body": json.dumps({"message": "Invalid email or password."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"message": "Server Error."})
        }
