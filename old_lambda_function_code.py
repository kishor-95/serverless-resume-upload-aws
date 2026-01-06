import boto3
import uuid
import datetime
import base64
import cgi
from io import BytesIO

# AWS clients
s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb")
sns = boto3.client("sns")

# CONFIG
UPLOAD_BUCKET = "resume-uploads-kishor-2002"   # Replace with your S3 bucket name
TABLE_NAME = "ResumeUploads"               # Replace with your DynamoDB table name          
TOPIC_ARN = "arn:aws:sns:us-east-1:778465394744:resume-upload-alerts"   # Replace with your SNS Topic ARN   

MAX_FILE_SIZE_MB = 5
ALLOWED_CONTENT_TYPE = "application/pdf"

table = ddb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print("Incoming request")

    body = event.get("body")
    if not body:
        return response(400, "Request body missing")

    # Decode body
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body)

    # Parse multipart/form-data
    content_type = event["headers"].get("content-type") or event["headers"].get("Content-Type")
    environ = {
        "REQUEST_METHOD": "POST",
        "CONTENT_TYPE": content_type
    }

    form = cgi.FieldStorage(
        fp=BytesIO(body),
        environ=environ,
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
        return response(400, "File size exceeds 5 MB limit")

    # Generate file name
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

    # Notify via SNS
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

    return response(200, "Resume uploaded successfully")

def response(status, msg):
    return {
        "statusCode": status,
        "body": msg
    }