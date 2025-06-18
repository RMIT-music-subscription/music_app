import json
import base64
import datetime
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.client("dynamodb")

def generate_jwt(user):
    email = user["email"]["S"]
    username = user["user_name"]["S"]
    expiration = (datetime.datetime.utcnow() + datetime.timedelta(days=2)).isoformat()

    payload = {
        "email": email,
        "username": username,
        "exp": expiration
    }

    json_payload = json.dumps(payload).encode("utf-8")
    base64_payload = base64.b64encode(json_payload).decode("utf-8")

    return {"token": base64_payload, "userName": username}

def verify_token(token):
    try:
        decoded_json = base64.b64decode(token).decode("utf-8")
        payload = json.loads(decoded_json)

        exp_time = datetime.datetime.fromisoformat(payload["exp"])
        if datetime.datetime.utcnow() > exp_time:
            raise Exception("Token expired")

        email = payload.get("email")
        response = dynamodb.get_item(
            TableName="login",
            Key={"email": {"S": email}}
        )

        if "Item" not in response:
            raise Exception("User not found")

        return {"valid": True, "user": payload}

    except Exception as e:
        return {"valid": False, "error": str(e)}

