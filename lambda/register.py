from botocore.exceptions import ClientError
# Remove
from aws_cred import AWS
table = AWS.aws_connect('dynamodb')

# table = boto3.client('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        email = event.get("emailAddress")
        username = event.get("userName")
        password = event.get("password")

        # Validate input
        if not email or not username or not password:
            raise Exception("Missing required fields: email, username, or password", 400)
        
        # Insert user into DynamoDB
        table.put_item(
            TableName="login",
            Item={
                "emailAddress": {"S": email},
                "userName": {"S": username},
                "password": {"S": password}
            },
            ConditionExpression="attribute_not_exists(emailAddress)"
        )
        
        # Return success response
        return {"statusCode": 201, "body": "User registered successfully"}
    except ClientError as e:
            error_message = e.response["Error"]["Message"]
            return {"statusCode":500,"body":{"error": f"AWS DynamoDB Error: {error_message}"}}
    except Exception as e:
        return {
            "statusCode": e.args[1] if len(e.args) > 1 else 500, 
            "body": {"error": str(e.args[0] if len(e.args) > 0 else 'Internal error. Try again')}
        }

# Example usage
# Remove 
# lambda_handler({
#     "emailAddress": "aswinKumar@gmail.com",
#     "userName": "aswinKumar",
#     "password": "aswin1234"
# }, None)