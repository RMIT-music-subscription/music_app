
import base64
import datetime
import json
from aws_cred import AWS

dynamodb = AWS.aws_connect('dynamodb')

def verify_token(token):
    try:
        decoded_json = base64.b64decode(token).decode("utf-8")
        payload = json.loads(decoded_json)

        exp_time = datetime.datetime.fromisoformat(payload["exp"])
        # if datetime.datetime.utcnow() > exp_time:
        #     raise Exception("Token expired")

        email = payload.get("email")
        response = dynamodb.get_item(
            TableName="login",
            Key={"emailAddress": {"S": email}}
        )

        if "Item" not in response:
            raise Exception("User not found")

        return {"valid": True, "user": payload}

    except Exception as e:
        return {"valid": False, "error": str(e)}


def lambda_handler(event, context):
    try:
        token = event.get("token")
        if not token:
            raise Exception("Token is required", 400)

        result = verify_token(token)
        if not result["valid"]:
            raise Exception(result["error"], 401)

        user = result["user"]["email"]
        # Get the PK and SK
        title = event.get("title")
        album = event.get("album")
        add = event.get("add")
        print(f"User: {user}, Title: {title}, Album: {album}, Add: {add}")
        if not title or not album:
            raise Exception("Title and album are required", 400)
        if add == True:
            dynamodb.put_item(
                TableName="subscribe",
                Item={
                    "emailAddress": {"S": user},
                    "title#album": {"S": f"{title}#{album}"}
                },
                ConditionExpression="attribute_not_exists(emailAddress) AND attribute_not_exists(#title_album)",
                ExpressionAttributeNames={
                    "#title_album": "title#album"
                }
            )
        else:
            # If add is False, we assume we want to delete the item
            dynamodb.delete_item(
                TableName="subscribe",
                Key={
                    "emailAddress": {"S": user},
                    "title#album": {"S": f"{title}#{album}"}
                },
                ConditionExpression="attribute_exists(emailAddress) AND attribute_exists(#title_album)",
                ExpressionAttributeNames={
                    "#title_album": "title#album"
                }
            )

        return {
            "statusCode": 200,
            "body": "Success"
        }

    except Exception as e:
        print(f"Error: {e}")
        print(f"Error querying music table: {str(e)}")
        return {
            "statusCode": e.args[1] if len(e.args) > 1 else 500,
            "body": {"error": str(e.args[0] if len(e.args) > 0 else 'Internal error. Try again')}
        }

lambda_handler({
    "token": "eyJlbWFpbCI6ICJhc3dpbkt1bWFyQGdtYWlsLmNvbSIsICJ1c2VybmFtZSI6ICJhc3dpbkt1bWFyIiwgImV4cCI6ICIyMDI1LTA2LTIwVDAxOjQwOjU3LjUyNzI2MCJ9",
    "title": "Trying to Reason with Hurricane Season",
    "album": "A1A",
    "add": False  # Set to False to delete the item
}, None)  # Example usage, remove in production