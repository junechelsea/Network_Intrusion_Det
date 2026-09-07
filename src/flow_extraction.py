
from scapy.all import sniff, IP, TCP, UDP
import csv
import os
from collections import defaultdict


# File where the dataset will be saved
output_file = "data/network_flows.csv"

# Make sure the data folder exists
os.makedirs("data", exist_ok=True)


print("Starting network traffic capture...")
print("Capturing 500 packets...\n")


# Capture network packets
packets = sniff(count=500)


print("\nCapture complete!")
print(f"Packets captured: {len(packets)}")


# Store packets belonging to the same flow
flows = defaultdict(list)


# ------------------------------------------------
# GROUP PACKETS INTO BIDIRECTIONAL FLOWS
# ------------------------------------------------

for packet in packets:

    # We need IPv4 information
    if IP not in packet:
        continue

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst


    # TCP traffic
    if TCP in packet:

        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        protocol = "TCP"


    # UDP traffic
    elif UDP in packet:

        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        protocol = "UDP"


    # Ignore other protocols for now
    else:
        continue


    # Create two endpoints
    endpoint1 = (src_ip, src_port)
    endpoint2 = (dst_ip, dst_port)


    # Sort endpoints so that both directions
    # belong to the same flow
    endpoints = tuple(sorted([endpoint1, endpoint2]))


    flow_key = (
        endpoints[0],
        endpoints[1],
        protocol
    )


    # Add packet to the flow
    flows[flow_key].append(packet)


# ------------------------------------------------
# EXTRACT FEATURES
# ------------------------------------------------

rows = []


for flow_key, flow_packets in flows.items():

    endpoint_a, endpoint_b, protocol = flow_key

    endpoint_a_ip, endpoint_a_port = endpoint_a
    endpoint_b_ip, endpoint_b_port = endpoint_b


    # Total packets
    packet_count = len(flow_packets)


    # Total bytes
    total_bytes = sum(len(packet) for packet in flow_packets)


    # Flow duration
    start_time = min(float(packet.time) for packet in flow_packets)
    end_time = max(float(packet.time) for packet in flow_packets)

    duration = end_time - start_time


    # Directional packet and byte counts
    forward_packets = 0
    backward_packets = 0

    forward_bytes = 0
    backward_bytes = 0


    for packet in flow_packets:

        packet_src = packet[IP].src
        packet_dst = packet[IP].dst


        if (
            packet_src == endpoint_a_ip
            and packet_dst == endpoint_b_ip
        ):

            forward_packets += 1
            forward_bytes += len(packet)

        else:

            backward_packets += 1
            backward_bytes += len(packet)


    # ------------------------------------------------
    # TCP FLAGS
    # ------------------------------------------------

    syn_count = 0
    ack_count = 0
    fin_count = 0
    rst_count = 0


    for packet in flow_packets:

        if TCP in packet:

            flags = packet[TCP].flags


            if "S" in flags:
                syn_count += 1


            if "A" in flags:
                ack_count += 1


            if "F" in flags:
                fin_count += 1


            if "R" in flags:
                rst_count += 1


    # ------------------------------------------------
    # TRAFFIC RATES
    # ------------------------------------------------

    if duration > 0:

        packets_per_second = packet_count / duration
        bytes_per_second = total_bytes / duration

    else:

        packets_per_second = packet_count
        bytes_per_second = total_bytes


    # ------------------------------------------------
    # ADD FLOW TO DATASET
    # ------------------------------------------------

    rows.append([
        endpoint_a_ip,
        endpoint_a_port,
        endpoint_b_ip,
        endpoint_b_port,
        protocol,
        packet_count,
        forward_packets,
        backward_packets,
        total_bytes,
        forward_bytes,
        backward_bytes,
        round(duration, 6),
        round(packets_per_second, 2),
        round(bytes_per_second, 2),
        syn_count,
        ack_count,
        fin_count,
        rst_count
    ])


# ------------------------------------------------
# SAVE DATASET
# ------------------------------------------------

with open(output_file, "w", newline="") as file:

    writer = csv.writer(file)


    # Dataset columns
    writer.writerow([
        "endpoint_a_ip",
        "endpoint_a_port",
        "endpoint_b_ip",
        "endpoint_b_port",
        "protocol",
        "packet_count",
        "forward_packets",
        "backward_packets",
        "total_bytes",
        "forward_bytes",
        "backward_bytes",
        "duration",
        "packets_per_second",
        "bytes_per_second",
        "syn_count",
        "ack_count",
        "fin_count",
        "rst_count"
    ])


    writer.writerows(rows)


print(f"\nFlow dataset saved to: {output_file}")
print(f"Number of bidirectional flows: {len(rows)}")

