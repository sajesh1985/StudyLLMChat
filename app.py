import json
import boto3
import time
from datetime import datetime
import streamlit as st

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

    # Create DynamoDB client
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table("chat-response-d")

    st.title("Save Message to DynamoDB")

    user_id = st.text_input("User ID")
    message_input = st.text_area("Message")

    if st.button("Save"):
        if not user_id or not message_input:
            st.error("Please enter both user_id and message")
        else:
            item = {
                "id": "678",
                "interactionId": "3456885484dfsw3",
                "input": message_input,
                "metric": 9,
                "response": reply
            }

            table.put_item(Item=item)
            st.success("Message saved successfully!")

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
