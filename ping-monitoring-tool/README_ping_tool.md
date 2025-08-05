
# Ping Monitoring Tool

This is a simple Python script that uses the `pingparsing` library to ping a given host (e.g., google.com, github.com) and display useful statistics such as packet loss, average round-trip time (RTT), and more.

## 📦 Requirements

- Python 3.x
- pingparsing (Install using `pip install pingparsing`)

## ▶️ How to Run

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the script with:

```
python ping_monitor.py
```

4. When prompted, enter a hostname or IP address (e.g., `google.com`, `8.8.8.8`).

## 🧪 Example Output

```
Enter the host to ping (e.g., google.com): github.com
Pinging github.com...

📊 Ping Statistics:
Target Host       : github.com
Packet Loss       : 0.0%
Average RTT       : 43.0 ms
Minimum RTT       : 33.0 ms
Maximum RTT       : 77.0 ms
Standard Deviation: None ms
```

## 📁 Folder Name Suggestion

`ping-monitoring-tool`

