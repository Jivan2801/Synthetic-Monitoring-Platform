import yaml
import time
import sys
import pingparsing
from typing import List, Dict

def load_config(path: str) -> Dict:
    try:
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
            if not isinstance(data, dict):
                raise ValueError("YAML root should be a dictionary.")
            if 'servers' not in data or 'interval' not in data:
                raise KeyError("YAML must contain 'servers' and 'interval'.")
            if not isinstance(data['servers'], list) or not isinstance(data['interval'], int):
                raise TypeError("'servers' should be a list and 'interval' should be an integer.")
            if not data['servers']:
                raise ValueError("Server list is empty. Add at least one server to ping.")
            return data
    except Exception as e:
        print(f"Failed to load config: {e}", file=sys.stderr)
        sys.exit(1)

def ping_host(host: str):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = host
    transmitter.count = 5

    try:
        result = transmitter.ping()
        stats = ping_parser.parse(result.stdout).as_dict()

        print(f"\n📡 Pinging {host}")
        if stats['packet_loss_rate'] is None:
            print(f"  Unable to ping {host} — No response or invalid host.")
            return

        print(f"  Packet Loss       : {stats['packet_loss_rate']}%")
        print(f"  Average RTT       : {stats['rtt_avg']} ms")
        print(f"  Minimum RTT       : {stats['rtt_min']} ms")
        print(f"  Maximum RTT       : {stats['rtt_max']} ms")
        print(f"  Std Deviation RTT : {stats['rtt_mdev']} ms")
        print()  

    except Exception as e:
        print(f"  Error pinging {host}: {e}")
        print()

def monitor(config_path: str):
    config = load_config(config_path)
    servers: List[str] = config['servers']
    interval: int = config['interval']

    print("🚀 Starting Ping Monitor...\n")
    try:
        while True:
            print(f"Round started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            for server in servers:
                ping_host(server)
            print(f"Waiting {interval} seconds before next round...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ping_monitor.py <config.yaml>", file=sys.stderr)
        sys.exit(1)
    monitor(sys.argv[1])
