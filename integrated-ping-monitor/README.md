# Integrated Ping Monitor

This tool reads a YAML configuration file containing a list of servers and a time interval, and then continuously pings each server at the specified interval. It displays key ping metrics like packet loss and round-trip time (RTT) for each server.

## Config File Format (`config.yaml`)

```yaml
servers:
  - google.com
  - github.com
interval: 10
```

- `servers`: List of server hostnames to ping
- `interval`: Time interval (in seconds) between ping rounds

## How to Run

```bash
python ping_monitor.py config.yaml
```

## Stop Monitoring

Press `Ctrl + C` to stop the program at any time.
