# 🛰️ Synthetic Ping Monitoring with Prometheus & Grafana

This project is a **Ping Monitoring Tool** that uses Python, Prometheus, and Grafana to continuously measure latency, packet loss, and availability of multiple servers. The results are exposed as metrics, scraped by Prometheus, and visualized in Grafana dashboards.

---

## 📦 Features
- 🐍 **Python Exporter**: Collects ping statistics using `pingparsing` and exposes them on `http://localhost:8989/metrics`.  
- 📄 **YAML Config Support**: Easily define servers and ping interval in `config.yaml`.  
- 📊 **Prometheus Integration**: Stores and queries metrics.  
- 📉 **Grafana Dashboards**:  
  - **Graph Panel** → Latency trends (`ping_rtt_avg_ms`).  
  - **Gauge Panel** → Availability/Latency with color-coded thresholds.  
- 🚨 **Alert Rules (rules.yml)**: Detects downtime, high latency, or packet loss.

---

## System Architecture
![System Architecture](./Grafana%20Dashboards/system-architecture.png)

---

## ⚙️ Requirements
- Python 3.x  
- Prometheus  
- Grafana  
- Python libraries:  
  ```bash
  pip install pingparsing pyyaml prometheus_client
  ```

---

## ▶️ How to Run

1. **Clone the repo** and go to your project folder.  
2. **Update servers list** in `config.yaml`:  
   ```yaml
   servers:
     - google.com
     - github.com
     - wikipedia.org
     - microsoft.com
   interval: 10
   ```  
3. **Run the Python exporter**:  
   ```bash
   python ping_monitor_prom.py config.yaml
   ```
   Metrics exposed on: `http://localhost:8989/metrics`  

4. **Start Prometheus**:  
   ```bash
   ./prometheus --config.file=prometheus.yml
   ```

5. **Start Grafana**:  
   - Open Grafana → `http://localhost:3000`  
   - Default login: `admin / admin`  

6. **Add Prometheus as a Data Source** (`http://localhost:9090`).  
7. **Import/Create Dashboards**:
   - Graph Panel → `ping_rtt_avg_ms` (time-series latency trends).  
   - Gauge Panel →  
     - `ping_success * 100` (availability, 0% = down, 100% = up)  
     - OR `ping_rtt_avg_ms` (live fluctuating latency).  

---

## 🚨 Alerts
Defined in `rules.yml`:
- **HostDown** → If a server is unreachable.  
- **HighLatency** → If RTT > threshold.  
- **PacketLossHigh** → If packet loss exceeds safe limits.  

---

## ✅ Summary
This project demonstrates how to integrate **Python, Prometheus, and Grafana** into a simple **Synthetic Monitoring Platform**. It helps visualize server health at a glance and provides early alerts for downtime or degraded performance.
