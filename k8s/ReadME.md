☸️ Kubernetes & Minikube: Automation & Networking Deep Dive
This documentation explains how we bridge the gap between Instance A (Jenkins) and Instance B (Kubernetes), and the engineering logic used to expose a private cluster to the internet.

1. Automated SSH Connection (Instance A to B)
For the pipeline to deploy code, the Jenkins CI/CD server must execute commands on the remote Kubernetes server.

Tool: SSH Agent Plugin

Why: Automation cannot "type" passwords. This plugin holds the .pem private key in the Jenkins memory securely.

Navigation:

Go to Manage Jenkins > Credentials.

Add SSH Username with private key (ID: k8s_auth).

Implementation:

Groovy
sshagent(['k8s_auth']) {
    sh "ssh -o StrictHostKeyChecking=no ubuntu@${IP} 'kubectl apply -f k8s/'"
}
Key Flag: -o StrictHostKeyChecking=no prevents the connection from hanging by bypassing the manual "trust this host" prompt.

2. Minikube: The Cluster Engine
Minikube is our local Kubernetes cluster running inside an AWS EC2 instance.

Role: It provides the environment (Control Plane, Nodes) to run our Docker containers.

Command: minikube start --driver=docker

Why Docker Driver?: It is the most resource-efficient way to run K8s inside an Ubuntu EC2 instance for CI/CD demos.

3. Port-Forwarding: Networking Deep Dive 🚀
This is the most critical stage. By default, Kubernetes pods/services have private IPs. Port-forwarding creates a "Tunnel" from the EC2 Public IP to the internal Cluster Service.

The Master Command:

Bash
nohup sudo -E kubectl port-forward --address 0.0.0.0 service/python-app-service 30007:80 > /tmp/k8s_forward.log 2>&1 &
Detailed Flag Explanation (Why we used them):

--address 0.0.0.0:

Default behavior: Listens only on 127.0.0.1 (localhost).

Our requirement: We need the world to see it. 0.0.0.0 tells the server to listen on all network interfaces, mapping the tunnel to the EC2's Public IP.

30007:80:

This maps Port 30007 of the EC2 (Host) to Port 80 of the K8s Service (Target).

nohup (No Hang Up):

The Problem: Jenkins kills all background processes once a job finishes.

The Solution: nohup ensures the tunnel stays alive even after Jenkins disconnects.

sudo -E:

sudo is required for port binding. -E (Preserve Environment) is vital so kubectl can still find the Minikube configuration files (stored in the user's home directory).

> /tmp/k8s_forward.log 2>&1 &:

Redirects all logs to a file and pushes the process to the background so the pipeline can finish successfully.

4. Troubleshooting & Self-Healing
Scenario A: Port is already in use

If you run the pipeline twice, the second build will fail because the port is blocked. We solve this with:

Bash
sudo fuser -k 30007/tcp || true
Logic: This finds the Process ID (PID) using the port, kills it, and clears the way for the new deployment.

Scenario B: App not loading in Browser

Check Process: ps aux | grep port-forward (If it's not there, the tunnel crashed).

Check Logs: cat /tmp/k8s_forward.log (Look for service name errors).

Check AWS: Ensure Port 30007 is open in your AWS Security Group (Inbound Rules).

5. Summary Flow
Jenkins logs in via SSH Agent.

Old Tunnels are cleared using fuser.

Minikube is verified/started.

K8s Manifests are applied.

A New Tunnel is created using nohup on 0.0.0.0.

Maintained by: Ajay Patel

Purpose: Permanent Documentation for DevOps Learning & Auditing. ✅