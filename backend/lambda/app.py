import json
import boto3

bedrock = boto3.client("bedrock-runtime")
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    message = body.get("message", "")

    if not message:
        return response(400, "Message is required")

    result = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 400
        })
    )

    data = json.loads(result["body"].read())
    reply = data["content"][0]["text"]

    return response(200, reply)

def response(code, msg):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"reply": msg})
    }
