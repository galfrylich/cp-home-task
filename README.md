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
  
