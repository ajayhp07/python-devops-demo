# 🚀 Automated DevSecOps Pipeline: End-to-End K8s Deployment

This repository contains a professional-grade CI/CD pipeline that automates a Python application from GitHub to a self-healing **Kubernetes (Minikube)** cluster on AWS. It features "Shift-Left" security, automated networking handshakes, and full-stack observability.

---

## 🏗️ 1. Infrastructure Architecture

We use a **Two-Instance Strategy** on AWS (Ubuntu 22.04) to mimic real-world production isolation.

### **Instance A: CI Server (The Builder)**

* **Role:** Orchestrates the pipeline, runs security scans, and builds artifacts.
* **Tools:** Jenkins, Docker, SonarQube.
* **Specs:** t2.medium (4GB RAM).

### **Instance B: CD Server (The Cluster)**

* **Role:** Hosts the Kubernetes cluster and the monitoring stack.
* **Tools:** Minikube, Prometheus, Grafana, Blackbox Exporter.
* **Specs:** t2.medium (2 vCPUs, 4GB RAM).

---

## 🤝 2. The "Handshake" (Connecting A to B)

The most critical technical challenge was enabling Jenkins (Instance A) to communicate with the K8s Server (Instance B) automatically.

### **The Authentication Flow:**

1. **SSH Key Exchange:** We stored Instance B’s `.pem` private key in Jenkins **Credentials** (ID: `k8s_auth`).
2. **SSH Agent Automation:** Used the **SSH Agent Plugin** to hold the key in memory during deployment.
3. **Security Group Handshake:** Instance B’s Security Group is configured to allow **Port 22 (SSH)** only from Instance A’s IP address.

**The Automation Logic:**

```groovy
sshagent(['k8s_auth']) {
    // '-o StrictHostKeyChecking=no' bypasses the manual "Yes/No" prompt for seamless automation
    sh "ssh -o StrictHostKeyChecking=no ubuntu@<INSTANCE_B_IP> 'kubectl apply -f k8s/'"
}

```

---

## 📡 3. Networking Deep Dive: Port Forwarding

Kubernetes pods are private by default. We used a "Background Tunneling" strategy to expose the app to the public internet.

### **The Implementation:**

```bash
nohup sudo -E kubectl port-forward --address 0.0.0.0 service/python-app-service 30007:80 > /tmp/k8s_forward.log 2>&1 &

```

* **`--address 0.0.0.0`**: Forces the tunnel to listen on the **EC2 Public IP** instead of just `localhost`.
* **`nohup` & `&**`: Ensures the tunnel stays alive even after the Jenkins job completes.
* **`sudo -E`**: Grants network permissions while preserving Minikube environment variables.
* **Self-Healing**: We use `sudo fuser -k 30007/tcp || true` before every deployment to kill old/blocked ports.

---

## 🚀 4. Installation & Setup Guide

### **Setup Instance A (CI Server)**

```bash
# Update & Install Docker + Jenkins
sudo apt update && sudo apt install docker.io jenkins -y
sudo usermod -aG docker ubuntu && newgrp docker

# Run SonarQube Container
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community

```

### **Setup Instance B (K8s & Monitoring)**

```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start --driver=docker

# Run Monitoring Stack (Prometheus/Grafana)
docker run -d --name node-exporter -p 9100:9100 prom/node-exporter
docker run -d --name grafana -p 3000:3000 grafana/grafana

```

---

## 📊 5. Observability Stack

We monitor the entire infrastructure to ensure 99.9% uptime.

* **Prometheus**: Configured via `prometheus.yml` to scrape targets using the Docker gateway IP `172.17.0.1`.
* **Blackbox Exporter**: Continuously probes the App URL for availability.
* **Grafana**: Visualizes metrics using **Dashboard ID: 1860**.

---

## 📂 6. Project Structure

```text
├── Jenkins/           # Pipeline Logic (Jenkinsfile)
├── docker/            # Application Containerization
├── k8s/               # K8s Deployment & Service Manifests
├── monitoring/        # Prometheus & Grafana Configuration
├── tests/             # Automated Functional Tests (Pytest)
└── app.py             # Python Flask Application

```

---
Automation Trigger Logic:

Primary Method: Configured GitHub Webhooks for instant "Push-based" triggers, ensuring zero delay between code commit and deployment.

Fallback Method: Implemented Poll SCM (H/2 * * * *) for environments where Jenkins is behind a private firewall, allowing the server to pull updates every 2 minutes.

## 🛡️ 7. Key Learning & Troubleshooting

* **Zero-Trust Security**: Implementing Security Groups and Private Key authentication.
* **Shift-Left**: Catching bugs and vulnerabilities using **SonarQube** and **Bandit** before deployment.
* **Log Analysis**: Using `/tmp/k8s_forward.log` to debug networking issues in real-time.

---

**Maintained by:** Ajay Patel

**Project Goal:** To demonstrate mastery in CI/CD, K8s Networking, and Automated Cloud Infrastructure. ✅

---
