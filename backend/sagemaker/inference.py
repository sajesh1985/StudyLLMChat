import boto3
import json

bedrock = boto3.client("bedrock-runtime")
prompt = st.chat_input("Ask a question")
def predict(prompt):
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps({
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        })
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]
