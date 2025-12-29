import streamlit as st
import boto3
import json

# ---------- CONFIG ----------
AWS_REGION = "us-east-1"
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
# ----------------------------

st.set_page_config(page_title="Bedrock Chat", layout="centered")

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("chat-response-d")

st.title("Chat + Save to DynamoDB")
# Bedrock client
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=AWS_REGION
)

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask a question...")

if prompt:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Claude request payload
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.7,
        "messages": [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
    }

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response["body"].read())
        full_response = result["content"][0]["text"]

        response_container.markdown(full_response)
        # Insert into DynamoDB
        item = {
            "id": "678", "interactionId": "3456885484dfsw3", "input": prompt, "metric": 9, "response": full_response
        }

        table.put_item(Item=item)

    # Store assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
