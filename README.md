# 🛰️ Synthetic Ping Monitoring with Prometheus, Grafana & Alertmanager  

This project is a **Ping Monitoring Tool** that uses Python, Prometheus, Grafana, and Alertmanager to continuously measure latency, packet loss, and availability of multiple servers.  
The results are exposed as metrics, scraped by Prometheus, visualized in Grafana dashboards, and **alert notifications are sent via email** using Alertmanager.  

---

## 📦 Features
- 🐍 **Python Exporter**: Collects ping statistics using `pingparsing` and exposes them on `http://localhost:8989/metrics`.  
- 📄 **YAML Config Support**: Easily define servers and ping interval in `config.yaml`.  
- 📊 **Prometheus Integration**: Stores and queries metrics.  
- 📉 **Grafana Dashboards**:  
  - **Graph Panel** → Latency trends (`ping_rtt_avg_ms`).  
  - **Gauge Panel** → Availability/Latency with color-coded thresholds.  
- 🚨 **Prometheus Alert Rules (rules.yml)**: Detects downtime, high latency, or packet loss.  
- 📧 **Email Notifications with Alertmanager**: Alerts are sent directly to your Gmail inbox when conditions are triggered.  

---

## 🏗 System Architecture
![System Architecture](./Grafana%20Dashboards/system-architecture.png)

---

## ⚙️ Requirements
- Python 3.x  
- Prometheus  
- Grafana  
- Alertmanager  
- Python libraries:  
  ```bash
  pip install pingparsing pyyaml prometheus_client
  ```

---

## ▶️ How to Run

### 1. Clone the repo & setup config  
Update servers list in `config.yaml`:  
```yaml
servers:
  - google.com
  - github.com
  - wikipedia.org
  - microsoft.com
interval: 10
```  

### 2. Run the Python Exporter  
```bash
python ping_monitor_prom.py config.yaml
```
Metrics exposed on: `http://localhost:8989/metrics`  

### 3. Start Prometheus  
```bash
./prometheus --config.file=prometheus.yml
```

Make sure your `prometheus.yml` has both **rules.yml** and **alertmanager.yml** references:  
```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets: ["localhost:9093"]

rule_files:
  - "rules.yml"

scrape_configs:
  - job_name: "ping_monitor"
    static_configs:
      - targets: ["localhost:8989"]
        labels:
          app: "prometheus"
```

### 4. Start Grafana  
- Open Grafana → `http://localhost:3000`  
- Default login: `admin / admin`  
- Add Prometheus as a Data Source (`http://localhost:9090`).  

### 5. Setup Grafana Dashboards  
- Create **Graph Panel** → Query: `ping_rtt_avg_ms` (time-series latency trends).  
- Create **Gauge Panel** → Query: `ping_success * 100` (availability).  

---

## 🚨 Alerts

### Prometheus Alert Rules (`rules.yml`)
- **HostDown** → If a server is unreachable.  
- **HighLatency** → If RTT > threshold.  
- **PacketLossHigh** → If packet loss exceeds safe limits.  

### Alertmanager Setup (`alertmanager.yml`)
Configure Alertmanager to send alerts via Gmail SMTP:  
```yaml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'your-email@gmail.com'
  smtp_auth_username: 'your-email@gmail.com'
  smtp_auth_password: 'your-app-password'  # Gmail App Password (not your normal password!)

route:
  receiver: 'email-alert'

receivers:
- name: 'email-alert'
  email_configs:
  - to: 'your-email@gmail.com'
    send_resolved: true
```

📌 **Important**:  
- Enable **2-Step Verification** in your Google account.  
- Generate a **Gmail App Password** and use it in place of your normal password.  

### Running Alertmanager
From the `prometheus-3.5.0.windows-amd64` folder (or your installation dir):  
```bash
./alertmanager --config.file=alertmanager.yml
```

Now, whenever an alert is triggered (e.g., host down, packet loss), you will **receive an email** instantly.

---

## ✅ Summary
This project demonstrates how to integrate **Python, Prometheus, Grafana, and Alertmanager** into a complete **Synthetic Monitoring Platform**.  
- 📊 Monitor latency & packet loss.  
- 🖥️ Visualize with Grafana dashboards.  
- 🚨 Trigger alerts with Prometheus rules.  
- 📧 Get real-time email notifications with Alertmanager.  
