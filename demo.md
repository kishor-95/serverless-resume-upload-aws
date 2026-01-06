Here is the complete `README.md` file, incorporating your provided introduction and architecture, and fully fleshing out the remaining sections (Workflow, Tech Stack, Deployment, etc.) to match the style.

```markdown
# Serverless Resume Upload Portal (AWS)

[![Build Status](https://img.shields.io/badge/build-stable-brightgreen.svg)](https://aws.amazon.com/)
[![Platform](https://img.shields.io/badge/platform-AWS-orange.svg)](https://aws.amazon.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Download](https://img.shields.io/badge/Download-Source_Code-red.svg)](#)

> **A fully serverless, scalable, and secure solution for collecting candidate resumes without managing a single server.**

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

## 🎯 Problem Statement

Organizations need a scalable, secure, and low-maintenance way to collect resumes from candidates. Traditional server-based systems introduce operational overhead, scaling challenges, and security risks.

**The Solution:** This project implements a fully serverless resume submission platform using AWS managed services. The backend validates input, securely stores files, persists metadata, and sends notifications — utilizing a pay-per-use model.

---

## 🏗 Architecture

The architecture utilizes a Lambda Function URL for a lightweight, API-Gateway-free entry point.

```mermaid
graph LR
    A[User / Browser] -->|HTTPS Upload| B[S3 Static Website]
    B -->|POST Request| C[Lambda Function URL]
    C -->|Store File| D[S3 Bucket (Private)]
    C -->|Write Metadata| E[DynamoDB]
    C -->|Trigger Alert| F[SNS Notification]
    F -->|Email| G[Admin]

```

---

## ⚡ Technology Stack

### **Frontend**

* **Core:** HTML5, JavaScript (ES6+)
* **Styling:** Tailwind CSS (via CDN for simplicity)
* **Hosting:** Amazon S3 (Static Website Hosting)

### **Backend & Infrastructure**

* **Compute:** AWS Lambda (Python 3.11)
* **API Exposure:** Lambda Function URL (Public Endpoint)
* **Storage:** Amazon S3 (Object Storage)
* **Database:** Amazon DynamoDB (NoSQL)
* **Notifications:** Amazon SNS (Simple Notification Service)
* **Security:** AWS IAM (Least Privilege Roles)
* **Monitoring:** Amazon CloudWatch

---

## 🔄 Workflow

1. **Submission:** The candidate uploads their resume (PDF) via the S3-hosted frontend.
2. **Transmission:** The browser sends a `POST` request with the file payload to the **Lambda Function URL**.
3. **Validation:** Lambda validates the file size (<5MB) and type (`application/pdf`).
4. **Storage:** The file is renamed with a UUID and stored in the private **Resume Uploads S3 Bucket**.
5. **Persistence:** Metadata (Timestamp, Original Filename, File ID) is saved to the **DynamoDB table**.
6. **Alert:** An **SNS** event triggers, sending an email notification to the recruitment admin.
7. **Response:** The user receives a success message on the frontend.

---

## ⚙️ Configuration

The Lambda function relies on the following Environment Variables:

| Variable | Purpose | Example Value |
| --- | --- | --- |
| `UPLOAD_BUCKET` | The S3 bucket where resumes are saved | `resume-uploads-prod-v1` |
| `DDB_TABLE` | The DynamoDB table name | `ResumeUploads` |
| `SNS_TOPIC_ARN` | The ARN for admin alerts | `arn:aws:sns:us-east-1:12345:alerts` |
| `MAX_FILE_MB` | File size limit in Megabytes | `5` |
| `ALLOWED_CONTENT_TYPE` | MIME type validation | `application/pdf` |

---

## 🚀 Deployment Guide

This project is deployed directly on AWS. Follow these manual steps or use the provided scripts.

### Step 1: Create S3 Buckets

**Frontend Bucket (Public):**

1. Create bucket: `resume-frontend-[unique-id]`
2. **Disable** "Block Public Access".
3. Enable **Static Website Hosting**.

**Upload Bucket (Private):**

1. Create bucket: `resume-uploads-[unique-id]`
2. **Enable** "Block Public Access" (Default).
3. Enable Server-Side Encryption (SSE-S3).

### Step 2: Database Setup

1. Create a DynamoDB table named **`ResumeUploads`**.
2. **Partition Key:** `resumeId` (String).
3. Use **On-Demand** capacity mode to save costs.

### Step 3: Notification System

1. Create an SNS Topic: `resume-upload-alerts`.
2. Create a Subscription -> Select Protocol: **Email**.
3. Enter your email and confirm the subscription via the link sent to your inbox.

### Step 4: Backend Logic

1. Create a Lambda Function (Python 3.11).
2. **Enable Function URL:**
* Auth Type: `NONE`
* CORS: Enable (Allow Origins `*`, Allow Methods `POST`).


3. Add the [Environment Variables](https://www.google.com/search?q=%23-configuration) listed above.
4. Deploy the Python code (see `src/lambda_function.py`).

### Step 5: IAM Permissions

Attach a policy to the Lambda execution role allowing:

* `s3:PutObject` on the **Upload Bucket**.
* `dynamodb:PutItem` on the **Table**.
* `sns:Publish` on the **SNS Topic**.

### Step 6: Frontend Integration

1. Update `index.html` with your specific **Lambda Function URL**.
2. Upload `index.html` to the **Frontend Bucket**.

---

## 🔒 Security & IAM

* **Least Privilege:** The Lambda role is restricted to only writing to specific resources.
* **Public Access:** Only the frontend static site is public; the storage bucket is strictly private.
* **Input Validation:** The backend rigorously checks file types to prevent malicious uploads (e.g., .exe files).

---

## 🛣 Roadmap

* [x] Core Upload Logic
* [x] Admin Email Alerts
* [ ] Add CAPTCHA to frontend to prevent spam
* [ ] Add User Authentication (Cognito) for candidates to view status
* [ ] Implement virus scanning on upload using ClamAV
* [ ] Infrastructure as Code (Terraform/SAM)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

```
