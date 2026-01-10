# 🚀 Python DevOps Demo

This project demonstrates a **basic DevOps workflow** using a containerized Python (Flask) application.
The focus of this phase is **Dockerization, image management, and deployment on an EC2 instance**.

---

## 📌 Project Overview

* Built a simple Flask web application
* Containerized the application using Docker
* Pushed the Docker image to Docker Hub
* Deployed and tested the application on an AWS EC2 instance
* Verified application accessibility via public IP

---

## 🔗 GitHub Repository

👉 [https://github.com/ajayhp07/python-devops-demo](https://github.com/ajayhp07/python-devops-demo)

---

## 🛠️ Technologies Used

* Python (Flask)
* Docker
* Docker Hub
* AWS EC2 (Ubuntu)
* Git & GitHub

---

## 📂 Project Structure

```
python-devops-demo/
│
├── docker/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   └── tests/
│
├── k8s/                # (to be used in next phase)
├── Jenkins/            # (planned)
├── monitoring/         # (planned)
└── README.md
```

---

## ⚙️ Work Done (Current Phase)

### 1️⃣ GitHub Setup

* Created a public GitHub repository
* Pushed application source code and Docker configuration

### 2️⃣ EC2 Setup

* Launched an Ubuntu EC2 instance
* Installed Docker and required dependencies
* Cloned the GitHub repository into the server

### 3️⃣ Docker Image Creation

* Wrote a Dockerfile for the Flask application
* Built Docker image:

  ```
  ajju121/python-devops-demo:v1
  ```

### 4️⃣ Docker Hub

* Logged in to Docker Hub from EC2
* Pushed the Docker image to Docker Hub
* Verified image availability by pulling it again

### 5️⃣ Container Testing

* Ran the container on EC2
* Exposed port `5000`
* Verified application using browser and `curl`
* Confirmed health and metrics endpoints

---

## 🌐 Application Access

The application was successfully accessed using:

```
http://<EC2-PUBLIC-IP>:5000
```

Health check:

```
/health
```

Metrics endpoint:

```
/metrics
```

---

## 📸 Output

The application displays:

* Container hostname
* Server time
* Health status

(Screenshot attached in project documentation)

---

## 🚧 Next Steps (Planned)

* Jenkins CI/CD pipeline
* Kubernetes deployment
* Monitoring using Prometheus & Grafana

These will be added as the next phase of the project.

---

## ✅ Current Status

✔ Application running successfully in Docker
✔ Image pushed and pulled from Docker Hub
✔ Deployed and tested on AWS EC2

---

## 👤 Author

**Ajay Patel**
DevOps Intern | Learning CI/CD, Docker, Kubernetes, Cloud

