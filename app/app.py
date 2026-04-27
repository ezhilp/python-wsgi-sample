# import os
# import uuid
# import logging
# from flask import Flask, request, jsonify
# import boto3
# from botocore.exceptions import ClientError

# app = Flask(__name__)
# logging.basicConfig(level=logging.INFO)

# AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
# BEDROCK_AGENT_ID = os.environ["BEDROCK_AGENT_ID"]
# BEDROCK_AGENT_ALIAS_ID = os.environ["BEDROCK_AGENT_ALIAS_ID"]

# bedrock_agent_runtime = boto3.client(
#     "bedrock-agent-runtime",
#     region_name=AWS_REGION,
# )

# def extract_text(completion_events) -> str:
#     """
#     Bedrock Agent responses come back as an event stream.
#     This helper collects text from chunk bytes.
#     """
#     parts = []

#     for event in completion_events:
#         chunk = event.get("chunk")
#         if chunk and "bytes" in chunk:
#             try:
#                 parts.append(chunk["bytes"].decode("utf-8"))
#             except Exception:
#                 pass

#         # Optional: inspect trace, files, returnControl, etc.
#         # trace = event.get("trace")
#         # files = event.get("files")
#         # return_control = event.get("returnControl")

#     return "".join(parts).strip()

# @app.post("/api/ask")
# def ask_agent():
#     # Trust this header only if traffic can come only from NGINX/LB.
#     user_email = request.headers.get("X-User-Email")
#     if not user_email:
#         return jsonify({"error": "Unauthorized: missing identity header"}), 401

#     body = request.get_json(silent=True) or {}
#     prompt = (body.get("message") or "").strip()

#     if not prompt:
#         return jsonify({"error": "message is required"}), 400

#     session_id = body.get("sessionId") or str(uuid.uuid4())

#     try:
#         response = bedrock_agent_runtime.invoke_agent(
#             agentId=BEDROCK_AGENT_ID,
#             agentAliasId=BEDROCK_AGENT_ALIAS_ID,
#             sessionId=session_id,
#             inputText=prompt,
#             enableTrace=False,
#             sessionState={
#                 "sessionAttributes": {
#                     "authenticated_user_email": user_email
#                 }
#             }
#         )

#         answer_text = extract_text(response["completion"])

#         return jsonify({
#             "sessionId": session_id,
#             "answer": answer_text
#         })

#     except ClientError as e:
#         app.logger.exception("Bedrock invoke failed")
#         return jsonify({
#             "error": "Bedrock invocation failed",
#             "details": e.response.get("Error", {}).get("Message", str(e))
#         }), 502
#     except Exception as e:
#         app.logger.exception("Unexpected error")
#         return jsonify({
#             "error": "Internal server error",
#             "details": str(e)
#         }), 500


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)