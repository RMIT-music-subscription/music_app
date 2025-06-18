import base64
import datetime
import json
import boto3
import re
from botocore.exceptions import ClientError

# dynamodb = boto3.client('dynamodb', region_name='us-east-1')
from aws_cred import AWS
dynamodb = AWS.aws_connect('dynamodb')

def validate_payload(data):
    # Extract fields
    password = data.get("password")
    username = data.get("user_name")
    email = data.get("emailAddress")

    # Email validation
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not email or not re.match(email_regex, email):
        raise Exception("Invalid email address", 400)

    # Password validation
    if not password:
        raise Exception("Enter password", 400)

    return (email, username, password)

def validate_user(data):
        # Retrieve user details from DynamoDB
        response = dynamodb.get_item(
            TableName="login",
            Key={"emailAddress": {"S": data.get("emailAddress")}}
        )
            
        # If the user is not found, return an error
        if "Item" not in response:
            raise Exception("User not found", 401)
        
        user = response["Item"]
        password = user["password"]["S"] 

        # Compare the decoded password with the input password
        if password != data.get("password"):
            raise Exception("Invalid password", 401)
        
        return response

def generate_jwt(user):
        """Generates a JWT token with a 2-day expiry"""

        email = user["emailAddress"]["S"]
        username = user["userName"]["S"]
       
        expiration = (datetime.datetime.utcnow() + datetime.timedelta(days=2)).isoformat()

        payload = {
            "email": email,
            "username": username,
            "exp": expiration
        }

        # Generating a token
        json_payload = json.dumps(payload)
        payload_bytes = json_payload.encode('utf-8')
        base64_payload = base64.b64encode(payload_bytes).decode('utf-8')

        return {"token":base64_payload, "userName": username}
        
def lambda_handler(event, context):
    try:
        body = event
        print(f"Body: {body}")
        validate_payload(body)
        response = validate_user(body)
        body = generate_jwt(response["Item"])
        print(f"Generated JWT: {body}")
        return {"statusCode": 201, "body": body}
    except ClientError as e:
            error_message = e.response["Error"]["Message"]
            print(f"AWS DynamoDB Error: {error_message}")
            return {"statusCode":500,"body":{"error": f"AWS DynamoDB Error: {error_message}"}}
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": e.args[1] if len(e.args) > 1 else 500, 
            "body": {"error": str(e.args[0] if len(e.args) > 0 else 'Internal error. Try again')}
        }

# Remove
lambda_handler({
    "emailAddress": "aswinKumar@gmail.com",
    "password": "aswin123"
}, None)