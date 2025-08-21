# Ping Monitor with Prometheus

This is a Python-based **Ping Monitoring Tool** that uses the `pingparsing` library to ping multiple servers (from a YAML config) and exposes the results as **Prometheus metrics**.  
Prometheus can then scrape these metrics, and alerts can be triggered using rules.

## 📦 Requirements

- Python 3.x  
- Install dependencies:
  ```bash
  pip install pingparsing PyYAML prometheus_client
  ```

## ▶️ How to Run

1. Open a terminal or command prompt.  
2. Navigate to the project directory (`ping-monitor-prometheus`).  
3. Run the exporter with:

   ```bash
   python ping_monitor_prom.py config.yaml
   ```

4. Metrics will be exposed at:  
   [http://localhost:8989/metrics](http://localhost:8989/metrics)

5. Start Prometheus (in `prometheus-3.5.0.windows-amd64`) with:

   ```bash
   .\prometheus.exe --config.file=prometheus.yml
   ```

6. Open the Prometheus UI at:  
   [http://localhost:9090](http://localhost:9090)

---

## 🧪 Example config.yaml

```yaml
servers:
  - google.com
  - github.com
  - invalid.domain
interval: 10
```

---

## 📊 Example Prometheus Metrics

```
ping_rtt_avg_ms{destination="google.com"} 11.0
ping_rtt_avg_ms{destination="github.com"} 21.0
ping_rtt_avg_ms{destination="invalid.domain"} NaN

ping_packet_loss_rate{destination="google.com"} 0.0
ping_packet_loss_rate{destination="invalid.domain"} NaN

ping_success{destination="google.com"} 1.0
ping_success{destination="invalid.domain"} 0.0
```

---

This project demonstrates how to **monitor network availability and latency**, export metrics in Prometheus format, and set up **alerting rules** for downtime, latency, and packet loss.
