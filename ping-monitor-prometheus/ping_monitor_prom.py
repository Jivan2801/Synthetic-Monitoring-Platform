import sys
import time
import yaml
import pingparsing
from typing import Dict, List, Any, Optional
from prometheus_client import start_http_server, Gauge, Counter

PING_RTT_MIN_MS  = Gauge("ping_rtt_min_ms",  "Minimum RTT (ms)",              ["destination"])
PING_RTT_AVG_MS  = Gauge("ping_rtt_avg_ms",  "Average RTT (ms)",              ["destination"])
PING_RTT_MAX_MS  = Gauge("ping_rtt_max_ms",  "Maximum RTT (ms)",              ["destination"])
PING_RTT_MDEV_MS = Gauge("ping_rtt_mdev_ms", "RTT standard deviation (ms)",   ["destination"])
PING_LOSS_PCT    = Gauge("ping_packet_loss_rate", "Packet loss percent (0-100)", ["destination"])
PING_OK          = Gauge("ping_success", "1 if ping succeeded, else 0",        ["destination"])

PKT_TX_TOTAL     = Counter("ping_packet_transmit_total", "Packets transmitted", ["destination"])
PKT_RX_TOTAL     = Counter("ping_packet_receive_total",  "Packets received",    ["destination"])
PKT_DUP_TOTAL    = Counter("ping_packet_duplicate_total","Duplicate packets",   ["destination"])

def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("YAML root should be a dictionary.")
    if "servers" not in data or "interval" not in data:
        raise KeyError("YAML must contain 'servers' and 'interval'.")
    if not isinstance(data["servers"], list) or not isinstance(data["interval"], int):
        raise TypeError("'servers' must be a list and 'interval' an integer.")
    if not data["servers"]:
        raise ValueError("Server list is empty. Add at least one server to ping.")
    return data

def _set_gauge(g: Gauge, destination: str, value: Optional[float]) -> None:
    # If ping failed, set NaN so Prometheus knows it's missing
    try:
        v = float("nan") if value is None else float(value)
        g.labels(destination=destination).set(v)
    except Exception:
        g.labels(destination=destination).set(float("nan"))

def ping_once(host: str, count: int = 5) -> Dict[str, Any]:
    parser = pingparsing.PingParsing()
    tx = pingparsing.PingTransmitter()
    tx.destination = host
    tx.count = count

    result = tx.ping()
    stats = parser.parse(result.stdout).as_dict()
    return stats

def update_metrics_for_host(host: str, stats: Dict[str, Any]) -> None:
    # Success if packet_loss_rate is not None and < 100
    success = 1.0 if (stats.get("packet_loss_rate") is not None and stats["packet_loss_rate"] < 100.0) else 0.0
    PING_OK.labels(destination=host).set(success)

    # Gauges — set each scrape round (use NaN on failure)
    _set_gauge(PING_LOSS_PCT,    host, stats.get("packet_loss_rate"))
    _set_gauge(PING_RTT_MIN_MS,  host, stats.get("rtt_min"))
    _set_gauge(PING_RTT_AVG_MS,  host, stats.get("rtt_avg"))
    _set_gauge(PING_RTT_MAX_MS,  host, stats.get("rtt_max"))
    _set_gauge(PING_RTT_MDEV_MS, host, stats.get("rtt_mdev"))

    # Counters — only increment with valid integers
    tx = stats.get("packet_transmit") or 0
    rx = stats.get("packet_receive") or 0
    dup = stats.get("packet_duplicate_count") or 0
    if isinstance(tx, (int, float)) and tx >= 0:
        PKT_TX_TOTAL.labels(destination=host).inc(tx)
    if isinstance(rx, (int, float)) and rx >= 0:
        PKT_RX_TOTAL.labels(destination=host).inc(rx)
    if isinstance(dup, (int, float)) and dup >= 0:
        PKT_DUP_TOTAL.labels(destination=host).inc(dup)

def monitor(config_path: str, prom_port: int = 8989) -> None:
    cfg = load_config(config_path)
    servers: List[str] = cfg["servers"]
    interval: int = cfg["interval"]

    # Start Prometheus HTTP server
    start_http_server(prom_port)
    print(f"🚀 Prometheus metrics exposed on http://localhost:{prom_port}/metrics\n")

    try:
        while True:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Round @ {ts}")
            for host in servers:
                try:
                    stats = ping_once(host, count=5)
                    update_metrics_for_host(host, stats)

                    # Console summary (optional)
                    loss = stats.get("packet_loss_rate")
                    avg  = stats.get("rtt_avg")
                    print(f"  {host:<20} loss={loss}%  avg={avg}ms  ok={loss is not None and loss < 100.0}")
                except Exception as e:
                    # Mark failure in metrics
                    PING_OK.labels(destination=host).set(0)
                    for g in (PING_LOSS_PCT, PING_RTT_MIN_MS, PING_RTT_AVG_MS, PING_RTT_MAX_MS, PING_RTT_MDEV_MS):
                        g.labels(destination=host).set(float("nan"))
                    print(f"  {host:<20} ERROR: {e}")
            print(f"Sleeping {interval}s...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ping_monitor_prom.py <config.yaml>", file=sys.stderr)
        sys.exit(1)
    monitor(sys.argv[1], prom_port=8989)
