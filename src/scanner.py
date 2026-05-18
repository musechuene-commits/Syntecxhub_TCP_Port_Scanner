import socket
import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Create logs folder
os.makedirs("logs", exist_ok=True)
log_file = "logs/scan_results.txt"

# Banner
print("=" * 50)
print("      TCP PORT SCANNER - CYBERSECURITY TOOL")
print("=" * 50)

# Argument parser
parser = argparse.ArgumentParser(description="TCP Port Scanner")
parser.add_argument("--host", required=True, help="Target IP or domain")
parser.add_argument("--ports", default="1-100", help="Port range e.g. 1-1000")
parser.add_argument("--threads", type=int, default=50, help="Number of threads")

args = parser.parse_args()

target = args.host
start_port, end_port = map(int, args.ports.split("-"))
threads = args.threads

# Resolve hostname
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid host")
    exit()

# Clear previous scan results
with open(log_file, "w", encoding="utf-8") as file:
    file.write("TCP PORT SCAN RESULTS\n")
    file.write("=" * 40 + "\n")
    file.write(f"Target: {target}\n")
    file.write(f"Resolved IP: {target_ip}\n")
    file.write(f"Ports: {start_port}-{end_port}\n")
    file.write(f"Threads: {threads}\n")
    file.write(f"Started at: {datetime.now()}\n")
    file.write("=" * 40 + "\n\n")

print(f"\nScanning Target: {target} ({target_ip})")
print(f"Ports: {start_port}-{end_port}")
print(f"Threads: {threads}")
print(f"Started at: {datetime.now()}\n")


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

        with open(log_file, "a", encoding="utf-8") as file:
            file.write(output + "\n")

        sock.close()

    except Exception as error:
        error_message = f"Error on port {port}: {error}"
        print(error_message)

        with open(log_file, "a", encoding="utf-8") as file:
            file.write(error_message + "\n")


# Start scanning
with ThreadPoolExecutor(max_workers=threads) as executor:
    executor.map(scan_port, range(start_port, end_port + 1))

print("\nScan completed.")
print(f"Results saved to: {log_file}")