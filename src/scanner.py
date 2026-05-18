import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Banner
print("=" * 50)
print("      TCP PORT SCANNER - CYBERSECURITY TOOL")
print("=" * 50)

# Argument parser
parser = argparse.ArgumentParser(description="TCP Port Scanner")
parser.add_argument("--host", required=True, help="Target IP or domain")
parser.add_argument("--ports", default="1-100", help="Port range (e.g. 1-1000)")
parser.add_argument("--threads", type=int, default=50, help="Number of threads")

args = parser.parse_args()

target = args.host
start_port, end_port = map(int, args.ports.split("-"))
threads = args.threads

# Resolve hostname
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("❌ Invalid host")
    exit()

print(f"\nScanning Target: {target} ({target_ip})")
print(f"Ports: {start_port}-{end_port}")
print(f"Threads: {threads}")
print(f"Started at: {datetime.now()}\n")

# Logging
log_file = "logs/scan_results.txt"

import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os

os.makedirs("logs", exist_ok=True)

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            output = f"Port {port}: OPEN"
        else:
            output = f"Port {port}: CLOSED"

        print(output)

        with open(log_file, "a") as f:
            f.write(output + "\n")

        sock.close()

    except Exception as e:
        print(f"Error on port {port}: {e}")

# Start scanning
with ThreadPoolExecutor(max_workers=threads) as executor:
    executor.map(scan_port, range(start_port, end_port + 1))

print("\nScan completed.")