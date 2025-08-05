import pingparsing

def monitor_ping(host):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()

    transmitter.destination = host
    transmitter.count = 5  # number of ping attempts

    print(f"Pinging {host}...\n")
    
    try:
        result = transmitter.ping()
        stats = ping_parser.parse(result.stdout).as_dict()

        print("📊 Ping Statistics:")
        print(f"Target Host       : {host}")
        print(f"Packet Loss       : {stats['packet_loss_rate']}%")
        print(f"Average RTT       : {stats['rtt_avg']} ms")
        print(f"Minimum RTT       : {stats['rtt_min']} ms")
        print(f"Maximum RTT       : {stats['rtt_max']} ms")
        print(f"Standard Deviation: {stats['rtt_mdev']} ms")

    except Exception as e:
        print("❌ Error occurred while pinging:")
        print(str(e))

if __name__ == "__main__":
    host = input("Enter the host to ping (e.g., google.com): ").strip()
    if host:
        monitor_ping(host)
    else:
        print("⚠️ Please enter a valid host.")
