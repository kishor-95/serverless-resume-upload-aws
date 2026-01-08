import boto3
import uuid
import datetime
import base64
import cgi
import os
from io import BytesIO

# AWS clients
s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb")
sns = boto3.client("sns")

# CONFIG (ENV first, fallback to working values)
UPLOAD_BUCKET = os.getenv(
    "UPLOAD_BUCKET",
) ## Configure UPLOAD_BUCKET in your Lambda environment variables or paste the bucket name here directly for testing purposes.

TABLE_NAME = os.getenv(
    "DDB_TABLE",

) ## Configure DDB_TABLE in your Lambda environment variables or paste the table name here directly for testing purposes.

TOPIC_ARN = os.getenv(
    "SNS_TOPIC_ARN",
) ##  Configure SNS_TOPIC_ARN in your Lambda environment variables or paste the ARN here directly for testing purposes.

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_MB", "5")) # Default to 5 MB
ALLOWED_CONTENT_TYPE = os.getenv(
    "ALLOWED_CONTENT_TYPE",
    "application/pdf"
) # Default to PDF

table = ddb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print("Incoming request")

    body = event.get("body")
    if not body:
        return response(400, "Request body missing")

    # Decode body
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body)

    headers = event.get("headers") or {}
    content_type = headers.get("content-type") or headers.get("Content-Type")

    if not content_type or "multipart/form-data" not in content_type:
        return response(400, "Invalid Content-Type")

    form = cgi.FieldStorage(
        fp=BytesIO(body),
        environ={
            "REQUEST_METHOD": "POST",
            "CONTENT_TYPE": content_type
        },
        keep_blank_values=True
    )

    name = form.getvalue("name")
    email = form.getvalue("email")
    file_item = form["file"] if "file" in form else None

    if not name or not email or file_item is None:
        return response(400, "Missing required fields")

    # Validate file type
    if file_item.type != ALLOWED_CONTENT_TYPE:
        return response(400, "Only PDF files are allowed")

    file_bytes = file_item.file.read()
    file_size_mb = len(file_bytes) / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        return response(400, "File size exceeds limit")

    resume_id = str(uuid.uuid4())
    filename = f"{resume_id}.pdf"

    # Upload to S3
    s3.put_object(
        Bucket=UPLOAD_BUCKET,
        Key=filename,
        Body=file_bytes,
        ContentType=ALLOWED_CONTENT_TYPE
    )

    # Store metadata
    table.put_item(Item={
        "resumeId": resume_id,
        "name": name,
        "email": email,
        "filename": filename,
        "uploadedAt": datetime.datetime.utcnow().isoformat()
    })

    # SNS notification (NON-BLOCKING)
    try:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="New Resume Uploaded",
            Message=f"""
New resume uploaded

Name  : {name}
Email : {email}
File  : {filename}
Time  : {datetime.datetime.utcnow().isoformat()}
"""
        )
    except Exception as e:
        print("SNS failed:", str(e))

    return response(200, "Resume uploaded successfully")

def response(status, msg):
    return {
        "statusCode": status,
        "body": msg
    }

