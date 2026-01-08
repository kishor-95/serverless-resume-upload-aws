# Serverless Resume Upload Portal – Infrastructure

This repository contains the Terraform configurations to provision, configure, and manage the AWS infrastructure for the Serverless Resume Upload Portal.

The project demonstrates a Cloud-Native approach to infrastructure, prioritizing reproducibility, security, and automation. By decoupling the infrastructure lifecycle from the application code, this setup ensures a stable foundation for the serverless backend.

## 📖 Project Overview

This infrastructure supports a web application that allows users to upload resumes securely.

The backend handles file storage, metadata indexing, and notification dispatching without provisioning a single server.

## Key Features

- **Infrastructure as Code (IaC):** 100% of the AWS resources are defined in Terraform.
- **Serverless Architecture:** Utilizes AWS Lambda, S3, DynamoDB, and SNS.
- **Security First:** Implements Least Privilege IAM roles, CORS restrictions, and private storage buckets.
- **State Management:** Uses remote S3 backend with DynamoDB locking for team-safe deployments.

## 🏗 Architecture

| Component  | Resource Type           | Description                                                                 |
|------------|--------------------------|-----------------------------------------------------------------------------|
| Frontend   | S3 Bucket (Public)       | Hosts the static `index.html` with public read access.                      |
| Storage    | S3 Bucket (Private)      | Securely stores uploaded resume PDFs. Public access is strictly blocked.   |
| Compute    | AWS Lambda               | Python runtime exposed via a Function URL (HTTPS).                          |
| Database   | DynamoDB                 | Stores resume metadata (Timestamp, Email, Filename).                        |
| Messaging  | SNS Topic                | Publishes upload events for email notifications.                            |
| Security   | IAM & Policies           | Custom roles restricting Lambda to specific resources only.                 |

## 📂 Directory Structure

```text
terraform/
├── backend.tf    # Remote state S3 and locking configuration
├── provider.tf   # AWS Provider pinning (~> 5.0)
├── variables.tf  # Input variables for region and resource naming
├── main.tf       # Core resource definitions (S3, Lambda, DynamoDB, IAM)
└── outputs.tf    # Exported values (URLs, ARNs, Bucket names)
```

**Note:** `.terraform/` folders, provider plugins, and `.tfstate` files are git-ignored to prevent secrets leakage.

## 🛠 Infrastructure Details

### 1. State Management

- **Storage:** S3 Bucket (`tf-state-serverless-resume-upload`)
- **Locking:** DynamoDB Table (`terraform-state-lock`)
- **Encryption:** State file is encrypted at rest.

### 2. Compute (Lambda) & Lifecycle

- **Function URL:** Public HTTPS endpoint with strict CORS settings (POST only).
- **Lifecycle Rules:** `ignore_changes` configured for source code to allow CI/CD deployments.

### 3. Database Strategy

- **Billing Mode:** On-Demand (Pay-Per-Request)
- **Partition Key:** `resumeId`

### 4. Configuration Injection

```javascript
const LAMBDA_UPLOAD_URL = "https://...";
```

## 🔐 Security & Permissions

- S3: `PutObject` (Backend Bucket only)
- DynamoDB: `PutItem` (Resumes Table only)
- SNS: `Publish` (Upload Topic only)
- CloudWatch: Logs

Wildcard permissions are avoided.

## 🚀 Deployment Guide

### Prerequisites

- Terraform CLI v1.0+
- AWS credentials configured

### Steps

```bash
terraform init
terraform plan
terraform apply
```

### Cleanup

```bash
terraform destroy
```

## ⚠️ Scope & Limitations

- Lambda application code is deployed separately.
- SNS subscriptions are managed outside Terraform.
- Resume objects are not lifecycle-managed by Terraform.
