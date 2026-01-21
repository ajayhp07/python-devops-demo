📊 Master Guide: Infrastructure Observability with Prometheus & Grafana
This guide explains how we monitor our Python application and AWS EC2 server health. It covers the "What," "Why," and "How" of our monitoring stack.

1. The Tech Stack: What & Why?
We use four specialized tools to ensure our system is always healthy:

Prometheus: The Database & Collector. It "scrapes" (pulls) numerical data from different parts of our system and stores it.

Grafana: The Visualizer. It connects to Prometheus and turns raw numbers into beautiful, easy-to-read charts and dashboards.

Node Exporter: The Hardware Agent. It runs on the server to collect hardware metrics like CPU usage, RAM availability, and Disk space.

Blackbox Exporter: The Uptime Monitor. It checks if our application's website URL is actually reachable and responding to users.

2. Detailed Configuration & Commands
We run everything in Docker containers for consistency. Here are the exact commands used in our automation:

A. Deploying the Agents (Exporters)

Bash
# Node Exporter: Collects Server Hardware Data
docker run -d --name node-exporter --restart always -p 9100:9100 prom/node-exporter

# Blackbox Exporter: Checks if our App URL is "Live"
docker run -d --name blackbox_exporter --restart always -p 9115:9115 prom/blackbox-exporter
B. Deploying the Brain (Prometheus)

Prometheus needs a configuration file (prometheus.yaml) to know where to look for data.

Bash
# We mount our local .yaml file into the container using the -v flag
docker run -d --name prometheus --restart always -p 9090:9090 \
    -v /home/ubuntu/prometheus.yaml:/etc/prometheus/prometheus.yml prom/prometheus
3. Detailed Setup Navigation (Step-by-Step)
Step 1: Verify Targets in Prometheus

Open your browser and go to: http://<YOUR_EC2_IP>:9090/targets

Check: You should see three jobs: node-exporter, blackbox-uptime, and prometheus.

Status: All must show a green "UP" status. If they are "DOWN," check if the IP in prometheus.yaml is correct.

Step 2: Connect Prometheus to Grafana

Open Grafana: http://<YOUR_EC2_IP>:3000 (Default Login: admin/admin)

Go to Menu -> Administration -> Data Sources.

Click Add data source and select Prometheus.

In the Connection URL, type: http://172.17.0.1:9090 (This is the internal Docker gateway IP).

Scroll down and click Save & Test. You should see a green success message.

Step 3: Import the Dashboard

Go to Menu -> Dashboards -> New -> Import.

In the Import via grafana.com box, type ID: 1860 (The "Node Exporter Full" dashboard).

Click Load.

Select your Prometheus Data Source in the dropdown.

Click Import. Now you have live graphs for CPU, RAM, and Network!

4. Expert Tips (To avoid future trouble)
IP Management: Inside Docker, 172.17.0.1 usually refers to the Host (EC2) itself. Using this IP in your prometheus.yaml helps containers talk to each other.

Security Groups: Always ensure ports 3000 (Grafana) and 9090 (Prometheus) are open in your AWS Security Group settings, or you won't be able to see the dashboards in your browser.

Persistent Config: If you change prometheus.yaml, you must restart the Prometheus container for the changes to take effect: docker restart prometheus.

YAML Syntax: YAML is very sensitive to spaces. Ensure your targets are correctly formatted inside [ ] brackets.

2.5 The Configuration Brain: prometheus.yml Deep Dive
This file tells Prometheus which targets to "scrape" (pull data from). We use a mix of static IPs and the Docker Gateway IP (172.17.0.1).

The Full Configuration File

YAML
global:
  scrape_interval: 15s # How often to pull data. 15s is industry standard.

scrape_configs:
  # 1. Monitor Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # 2. Monitor EC2 Hardware (CPU, RAM, Disk)
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['172.17.0.1:9100']

  # 3. Monitor Application Uptime (URL check)
  - job_name: 'blackbox-uptime'
    metrics_path: /probe
    params:
      module: [http_2xx] # Look for a successful 200 OK response
    static_configs:
      - targets:
          - http://172.17.0.1:30007 # Your Python App URL
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 172.17.0.1:9115 # The Blackbox Exporter's real address
Why did we use these specific settings?

scrape_interval: 15s: If you set this too low (e.g., 1s), it puts too much load on your CPU. 15 seconds is the "sweet spot" for performance and accuracy.

172.17.0.1: This is the Docker Bridge IP. Since Prometheus is inside a container, it cannot use localhost to find the Node Exporter on the host. It must use this gateway IP to "talk" to the host machine.

Blackbox Relabeling: This is a bit advanced but very important. We tell Prometheus to send the "App URL" to the Blackbox Exporter on port 9115. The exporter then checks the site and tells Prometheus if it is UP or DOWN.

3. Detailed Setup Navigation (Step-by-Step)
Step 1: Verify Targets in Prometheus

Open your browser and go to: http://<YOUR_EC2_IP>:9090/targets

Check: You should see three jobs: node-exporter, blackbox-uptime, and prometheus.

Status: All must show a green "UP" status. If they are "DOWN," check if the IP in prometheus.yml is reachable.

4. Expert Tips (To avoid future trouble)
YAML Syntax: YAML does not allow Tabs. Always use Spaces. One wrong space can break the entire Prometheus container.

Dynamic Changes: If you add a new target to the .yml file, you must restart the container: docker restart prometheus.

Port Check: If a target is "DOWN," try running curl http://172.17.0.1:9100/metrics from your EC2 terminal. If you don't see numbers, the exporter is not running.

This Documentation is a permanent part of Ajay Patel's DevOps Portfolio. ✅