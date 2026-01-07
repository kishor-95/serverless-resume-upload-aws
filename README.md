# Serverless Resume Upload Portal (AWS)
---
## 📖 Table of Contents
- [Problem Statement](#-problem-statement)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Workflow](#-workflow)
- [Configuration](#-configuration)
- [Deployment Guide](#-deployment-guide)
- [Security & IAM](#-security--iam)
- [Roadmap](#-roadmap)

---

## 1. Problem Statement

Organizations require a scalable, secure, and low-maintenance mechanism to collect resumes from candidates. Traditional server-based solutions introduce operational overhead, scalability limitations, and increased security risks.

This project addresses these challenges by implementing a **fully serverless resume submission platform** using AWS managed services, eliminating server management while ensuring secure file handling, metadata persistence, and notification delivery.

---

## 2. Project Overview

The Serverless Resume Upload Portal enables candidates to submit resumes through a web interface. The backend validates inputs, securely stores resume files, records metadata, and sends administrative notifications — all using serverless AWS services.

The solution is designed to be cost-efficient, scalable, and production-ready.

---

## 3. Architecture Overview

User (Browser)  
→ Amazon S3 (Static Website – Frontend)  
→ AWS Lambda Function URL  
→ Amazon S3 (Resume Storage)  
→ Amazon DynamoDB (Metadata Storage)  
→ Amazon SNS (Admin Notification)

## Architecture Diagram
![Architecture Diagram](images/architecture.png)
---

## 4. Technology Stack

### Frontend
- HTML  
- Tailwind CSS  
- JavaScript  
- Amazon S3 (Static Website Hosting)

### Backend
- AWS Lambda (Python 3.11)  
- Lambda Function URL  
- Amazon S3  
- Amazon DynamoDB  
- Amazon SNS  
- AWS IAM  
- Amazon CloudWatch  

---

## 5. Runtime Execution Flow

1. User submits resume via the frontend form  
2. Browser sends a multipart/form-data request  
3. Lambda Function URL receives the HTTPS request  
4. Lambda validates user input and file constraints  
5. Resume file is stored in a private S3 bucket  
6. Metadata is written to DynamoDB  
7. SNS notification is sent to the administrator  
8. HTTP success response is returned to the user  

---

## 6. IAM Roles and Permissions

The Lambda function executes with a **least-privilege IAM role**. Required permissions include:

- `s3:PutObject` – restricted to the resume uploads bucket  
- `dynamodb:PutItem` – restricted to the ResumeUploads table  
- `sns:Publish` – restricted to the notification topic  
- CloudWatch Logs permissions – for logging and monitoring  

This design minimizes the blast radius and aligns with AWS security best practices.

---

## 7. Environment Variables

The application externalizes configuration using environment variables.

| Variable | Purpose |
|--------|--------|
| `UPLOAD_BUCKET` | S3 bucket for resume storage |
| `DDB_TABLE` | DynamoDB table name |
| `SNS_TOPIC_ARN` | SNS topic ARN |
| `MAX_FILE_MB` | Maximum allowed file size |
| `ALLOWED_CONTENT_TYPE` | Allowed resume file type |

---

## 8. How to Deploy

This project is deployed directly on AWS and is not intended to be run locally.

### Step 1: Create S3 Buckets

**Frontend Bucket (Public)**  
- Create an S3 bucket (e.g., `resume-frontend-unique`)  
- Disable “Block all public access”  
- Enable Static Website Hosting  
- Set `index.html` as the index document  

**Resume Upload Bucket (Private)**  
- Create an S3 bucket (e.g., `resume-uploads-unique`)  
- Keep “Block all public access” enabled  
- Enable default encryption  

---

### Step 2: Create DynamoDB Table

- Table name: `ResumeUploads`  
- Partition key: `resumeId` (String)  
- Billing mode: On-Demand  

---

### Step 3: Create SNS Topic

- Create an SNS topic (e.g., `resume-upload-alerts`)  
- Add an email subscription and confirm it  
- Copy the Topic ARN  

---

### Step 4: Create Lambda Function

- Runtime: Python 3.11  
- Paste the Lambda function code  
- Deploy the function  

---

### Step 5: Configure IAM Role

Attach an IAM role to the Lambda function with permissions for:
- `s3:PutObject`  
- `dynamodb:PutItem`  
- `sns:Publish`  
- CloudWatch Logs  

---

### Step 6: Configure Environment Variables

| Variable | Example |
|--------|--------|
| `UPLOAD_BUCKET` | resume-uploads-unique |
| `DDB_TABLE` | ResumeUploads |
| `SNS_TOPIC_ARN` | arn:aws:sns:region:account:resume-upload-alerts |
| `MAX_FILE_MB` | 5 |
| `ALLOWED_CONTENT_TYPE` | application/pdf |

---

### Step 7: Enable Lambda Function URL

- Authentication: NONE  
- Enable CORS (POST, *, *)  
- Copy the Function URL  

---

### Step 8: Deploy Frontend

- Update the API endpoint in `index.html` with the Lambda Function URL  
- Upload `index.html` to the frontend S3 bucket  
- Open the S3 Static Website URL  

---

### Step 9: Test Deployment

- Upload a PDF resume  
- Verify object creation in S3  
- Verify metadata entry in DynamoDB  
- Verify SNS email notification  

---

## 9. Monitoring and Logging

- Lambda execution logs are available in Amazon CloudWatch  
- SNS metrics can be monitored via CloudWatch  

---

## 10. Future Enhancements

- SES-based user confirmation emails  
- User authentication using Amazon Cognito  
- User dashboard for uploaded resumes  
- Infrastructure as Code using Terraform  

---

## 11. Project Status

Stable and operational.
