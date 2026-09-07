
from scapy.all import sniff, IP, TCP, UDP, ICMP
import csv
import os
from datetime import datetime


# Where our dataset will be saved
output_file = "data/network_traffic.csv"

# Create the data folder if it does not already exist
os.makedirs("data", exist_ok=True)


print("Starting packet capture...")
print("Capturing 50 packets...\n")

# Capture 50 packets
packets = sniff(count=50)

print("\nCapture complete!")
print(f"Packets captured: {len(packets)}\n")


# Store extracted features
rows = []


# Go through every captured packet
for packet in packets:

    # We only process packets that contain IPv4 information
    if IP not in packet:
        continue

    # Basic IP information
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    packet_length = len(packet)

    # Default values
    protocol = "OTHER"
    src_port = ""
    dst_port = ""
    tcp_flags = ""

    # TCP packet
    if TCP in packet:
        protocol = "TCP"
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        tcp_flags = str(packet[TCP].flags)

    # UDP packet
    elif UDP in packet:
        protocol = "UDP"
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport

    # ICMP packet
    elif ICMP in packet:
        protocol = "ICMP"

    # Save the extracted information
    rows.append([
        datetime.fromtimestamp(float(packet.time)).strftime("%Y-%m-%d %H:%M:%S"),
        src_ip,
        dst_ip,
        protocol,
        src_port,
        dst_port,
        packet_length,
        tcp_flags
    ])


# Create the CSV dataset
with open(output_file, "w", newline="") as file:

    writer = csv.writer(file)

    # Column headings
    writer.writerow([
        "timestamp",
        "src_ip",
        "dst_ip",
        "protocol",
        "src_port",
        "dst_port",
        "packet_length",
        "tcp_flags"
    ])

    # Write the extracted packet information
    writer.writerows(rows)


print(f"Dataset saved successfully to: {output_file}")
print(f"Records saved: {len(rows)}")

