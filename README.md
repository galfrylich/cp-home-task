# Email Processing Platform – AWS EKS (Terraform + Helm + CI/CD)

## 📌 Overview

This project implements a **2 microservices system** running on **Amazon EKS**, using:

- **Terraform** – infrastructure provisioning  
- **Docker** – containerization  
- **Helm** – Kubernetes deployments  
- **GitHub Actions** – CI/CD automation  
- **AWS managed services** – ALB, SQS, S3, SSM  

The system processes email payloads end-to-end with a clean separation between **infrastructure** and **application** layers.

---

## 🏗️ Architecture (IMPORTANT)

### ✅ Final Architecture (Actual Implementation)

Internet

↓

AWS Application Load Balancer (Terraform)

↓

ALB Listener :80

↓

ALB Target Group (type: instance, port: NodePort)

↓

EKS Worker Nodes

↓

Kubernetes Service (NodePort)

↓

Pods (service-1 API)

↓

Amazon SQS

↓

Pods (service-2 Worker)

↓

Amazon S3

---

## ❗ Key Design Decisions

| Component | Implementation |
|--------|----------------|
| ALB | Created by **Terraform** |
| Target Group | **instance** |
| Backend Port | **NodePort (30080)** |
| Kubernetes Service | **NodePort** |
| Ingress | ❌ Not used |
| Service type LoadBalancer | ❌ Not used |

The ALB is **external to Kubernetes** and forwards traffic **directly to EKS worker nodes**.

---

## 📦 Microservices

### service-1 (API)
- Python (FastAPI)
- Exposes `/send`
- Expose `/health` (for alb endpoint)
- Validates request payload
- Publishes messages to SQS

### service-2 (Worker)
- Python background worker
- Polls SQS
- Writes payloads to S3

---

## ☁️ AWS Resources (Terraform Managed)

- VPC + subnets  
- EKS cluster + node group  
- Application Load Balancer  
- Target Group (instance mode)  
- Security Groups  
- SQS queue  
- S3 bucket  
- SSM Parameter (JWT secret)  





## 🚀 CI/CD Pipeline (GitHub Actions)

### Pipeline Responsibilities

1. Build Docker images for both services  
2. Generate **one shared image tag** per commit  
3. Push images to Docker Hub  
4. Authenticate to AWS  
5. Configure kubeconfig for EKS  
6. Deploy Helm releases  
7. Run post-deployment smoke tests  

---

## ▶️ How to run this project (for reviewers)

### 1. Prerequisites

- Terraform, kubectl, and Helm installed locally  
- An AWS account with permissions to create VPC, EKS, ALB, SQS, S3, and SSM parameters  

### 2. Provision infrastructure with Terraform

From `iac/enviorments/dev`:

```bash
terraform init      # adjust backend in iac/backend.tf if needed
terraform apply -var="jwt_secret=$DJISA<$#45ex3RtYr"
```

This creates:

- EKS cluster `dev-eks`  
- SQS queue `dev-email-queue`  
- S3 bucket `dev-email-payloads-<your-account-id>`  
- SSM parameter `/dev/email-service/jwt-secret` with the shared token  
- Application Load Balancer pointing to the EKS NodePort service  

### 3. Configure kubectl for the new EKS cluster

```bash
aws eks update-kubeconfig --name dev-eks --region ca-central-1
```

### 4. Prepare Kubernetes AWS credentials secret

Create the `aws-creds` secret in the `email-services` namespace (same keys used by the Helm charts):

```bash
kubectl create namespace email-services || true
kubectl create secret generic aws-creds \
  -n email-services \
  --from-literal=AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY_ID> \
  --from-literal=AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>
```

### 5. CI/CD (GitHub Actions)

- Configure GitHub repository secrets:
  - `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
  - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- Push to `main` to trigger `.github/workflows/build-and-deploy.yml`:
  - Builds and pushes both Docker images  
  - Deploys `service-1` and `service-2` via Helm  
  - Runs a smoke test through the ALB  

### 6. Manual test of the API

After Terraform finishes, get the ALB DNS:

```bash
ALB_DNS=$(aws elbv2 describe-load-balancers \
  --region ca-central-1 \
  --query "LoadBalancers[?contains(LoadBalancerName,'service-1')].DNSName | [0]" \
  --output text)
```

Call the service using the exact exam payload format:

```bash
curl -X POST "http://$ALB_DNS/send" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "email_subject": "Happy new year!",
      "email_sender": "John doe",
      "email_timestream": "1693561101",
      "email_content": "Just want to say... Happy new year!!!"
    },
    "token": "$DJISA<$#45ex3RtYr"
  }'
```

`service-1` validates the token and fields, publishes to SQS, `service-2` pulls the message and uploads it to S3 under `emails/<yyyy>/<mm>/<dd>/...json`.
