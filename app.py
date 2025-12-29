import json
import boto3
import uuid
import streamlit as st
from datetime import datetime

# AWS clients
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("chat-response-d")
st.write("DEBUG VERSION: 2025-01-08-01")

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

st.title("Chat + Save to DynamoDB")
#prompt = st.chat_input("Ask a question")
message = st.text_area("Enter your message")

if st.button("Send"):
    if not message:
        st.error("Message is required")
    else:
        # Invoke Bedrock
        result = bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 400,
                "messages": [{"role": "user", "content": [{ "type": "text", "text": message }]}],
                "max_tokens": 400
            })
        )

        data = json.loads(result["body"].read())
        reply = data["content"][0]["text"]

        # Insert into DynamoDB
        item = {
            "id": "678", "interactionId": "3456885484dfsw3", "input": message, "metric": 9, "response": reply
        }

        table.put_item(Item=item)

        st.success("Saved to DynamoDB")
        st.write("Response:", reply)
