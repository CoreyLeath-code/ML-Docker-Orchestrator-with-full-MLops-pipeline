ML-Docker-Orchestrator with Full MLops Pipeline

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestrated-326ce5)
![MLflow](https://img.shields.io/badge/MLflow-Experiment_Tracking-0194E2)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-orange)
![CI/CD](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-success)
![FastAPI](https://img.shields.io/badge/FastAPI-Production_API-green)
![Terraform](https://img.shields.io/badge/Terraform-Infrastructure-623CE4)
![MLOps](https://img.shields.io/badge/MLOps-End_to_End-critical)



Architecture Flow

![image](https://github.com/user-attachments/assets/d9044d80-a9d7-42f7-8957-19bd2e9e9e77)



README
ML Docker Orchestrator – Production ML Inference Platform

A production-style ML inference orchestration system demonstrating full end-to-end MLOps:

Model training & experiment tracking

Containerized inference

CI/CD automation

Kubernetes deployment

Infrastructure as Code

Observability & monitoring

Scalable API serving

This project demonstrates how ML systems operate in real enterprise environments.

 System Architecture
User Request
     ↓
FastAPI Inference Layer
     ↓
Input Validation (Pydantic)
     ↓
Inference Pipeline
     ↓
Model Loader (Cached)
     ↓
Prediction Engine
     ↓
Metrics (Prometheus)
     ↓
Structured Logging
     ↓
Response

Parallel Systems:

Training Pipeline
     ↓
MLflow Experiment Tracking
     ↓
Model Registry
     ↓
Docker Build
     ↓
Kubernetes Deployment

Infrastructure:

Terraform → Kubernetes Cluster
Docker → Container Runtime
GitHub Actions → CI/CD
Prometheus → Monitoring
Core Features
Production Inference API

FastAPI-based scalable serving

Model caching for performance

Typed request/response schemas

MLOps Integration

MLflow experiment tracking

Model versioning

Environment config management

Containerization

Multi-stage Docker build

Production-ready image optimization

Orchestration

Kubernetes deployment manifests

Horizontal scaling ready

Observability

Prometheus metrics

Latency tracking

Request counters

Structured logging

CI/CD

GitHub Actions pipeline

Automated testing

Build validation



Metrics Table
Metric	Description	Purpose
ml_api_requests_total	Total API requests	Traffic monitoring
ml_prediction_latency_seconds	Inference latency	Performance tracking
model_version	Active model version	Traceability
experiment_id	MLflow run ID	Reproducibility
deployment_replicas	Active pods	Scaling insight





Quick Start
Clone Repository
git clone https://github.com/Trojan3877/ML-Docker-Orchestrator-with-full-MLops-pipeline.git
cd ML-Docker-Orchestrator-with-full-MLops-pipeline
Create Environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
 Run API
uvicorn api.main:app --reload



http://localhost:8000/docs
 Docker Run
docker build -t ml-orchestrator .
docker run -p 8000:8000 ml-orchestrator
 Kubernetes Deploy
kubectl apply -f orchestration/kubernetes/deployment.yaml
Metrics Table
Metric	Description	Purpose
ml_api_requests_total	Total API requests	Traffic monitoring
ml_prediction_latency_seconds	Inference latency	Performance tracking
model_version	Active model version	Traceability
experiment_id	MLflow run ID	Reproducibility
deployment_replicas	Active pods	Scaling insight
Enterprise Capabilities Demonstrated

Decoupled training and inference pipelines

Reproducible experiment tracking

Container-first deployment model

Infrastructure as Code (Terraform-ready)

Horizontal scalability via Kubernetes

Observability-first design

CI/CD-driven validation


Q1: How does this system handle model versioning?

Model artifacts are logged via MLflow and can be promoted to production through registry integration. Deployment is decoupled from training, allowing safe model upgrades.

Q2: How is inference latency controlled?

Model caching at startup

Prometheus latency monitoring

Container resource constraints

Horizontal pod scaling

Q3: How would you scale this for millions of requests?

Add API gateway layer

Implement Redis caching

Use autoscaling (HPA)

Add load balancing

Deploy on managed Kubernetes (EKS/GKE)

Q4: How is reproducibility ensured?

MLflow tracking URI

Logged hyperparameters

Artifact versioning

Environment config isolation

Q5: How would you integrate GPU support?

Use CUDA-enabled Docker base image

Kubernetes node selector for GPU nodes

Torch/TensorFlow GPU runtime

Q6: How would you improve fault tolerance?

Readiness and liveness probes

Circuit breaker pattern

Request timeouts

Graceful shutdown hooks

Q7: What makes this enterprise-grade?

Config-driven architecture

CI/CD validation

Observability integration

Decoupled pipelines

Infrastructure modularity

Production-style container builds

Why This Project Matters

This repository demonstrates:
Practical MLOps understanding
Infrastructure fluency
Production API design
DevOps integration
System design thinking
It is not a toy ML project.
It is an infrastructure-oriented ML platform.
