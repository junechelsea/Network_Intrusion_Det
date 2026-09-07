from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import os
from collections import defaultdict


CAPTURE_COUNT = 1000
OUTPUT_FILE = "data/attack_traffic.csv"


print("========================================")
print(" ATTACK TRAFFIC COLLECTION")
print("========================================")
print(f"Capturing {CAPTURE_COUNT} packets...")
print("Waiting for controlled scan traffic...")
print("")


packets = sniff(count=CAPTURE_COUNT)

print("\nCapture complete!")
print(f"Packets captured: {len(packets)}")


flows = defaultdict(list)


# Group packets into bidirectional flows
for packet in packets:

    if not packet.haslayer(IP):
        continue

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst

    if packet.haslayer(TCP):
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        protocol_name = "TCP"

    elif packet.haslayer(UDP):
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        protocol_name = "UDP"

    else:
        src_port = 0
        dst_port = 0
        protocol_name = str(packet[IP].proto)

    endpoint1 = (src_ip, src_port)
    endpoint2 = (dst_ip, dst_port)

    flow_key = tuple(sorted([endpoint1, endpoint2])) + (protocol_name,)

    flows[flow_key].append(packet)


records = []


for flow_key, flow_packets in flows.items():

    endpoint_a = flow_key[0]
    endpoint_b = flow_key[1]
    protocol_name = flow_key[2]

    start_time = float(flow_packets[0].time)
    end_time = float(flow_packets[-1].time)

    duration = end_time - start_time

    if duration <= 0:
        duration = 0.001

    packet_count = len(flow_packets)

    forward_packets = 0
    backward_packets = 0

    forward_bytes = 0
    backward_bytes = 0

    total_bytes = 0

    syn_count = 0
    ack_count = 0
    fin_count = 0
    rst_count = 0


    for packet in flow_packets:

        if not packet.haslayer(IP):
            continue

        packet_length = len(packet)
        total_bytes += packet_length

        if packet[IP].src == endpoint_a[0]:
            forward_packets += 1
            forward_bytes += packet_length
        else:
            backward_packets += 1
            backward_bytes += packet_length


        if packet.haslayer(TCP):

            flags = packet[TCP].flags

            if "S" in flags:
                syn_count += 1

            if "A" in flags:
                ack_count += 1

            if "F" in flags:
                fin_count += 1

            if "R" in flags:
                rst_count += 1


    packets_per_second = packet_count / duration
    bytes_per_second = total_bytes / duration


    records.append({
        "endpoint_a_ip": endpoint_a[0],
        "endpoint_a_port": endpoint_a[1],

        "endpoint_b_ip": endpoint_b[0],
        "endpoint_b_port": endpoint_b[1],

        "protocol": protocol_name,

        "packet_count": packet_count,

        "forward_packets": forward_packets,
        "backward_packets": backward_packets,

        "total_bytes": total_bytes,

        "forward_bytes": forward_bytes,
        "backward_bytes": backward_bytes,

        "duration": duration,

        "packets_per_second": packets_per_second,
        "bytes_per_second": bytes_per_second,

        "syn_count": syn_count,
        "ack_count": ack_count,
        "fin_count": fin_count,
        "rst_count": rst_count,

        "label": "SCAN"
    })


df = pd.DataFrame(records)

os.makedirs("data", exist_ok=True)


# Add new attack data to an existing attack dataset
if os.path.exists(OUTPUT_FILE):
    existing_df = pd.read_csv(OUTPUT_FILE)
    combined_df = pd.concat([existing_df, df], ignore_index=True)
else:
    combined_df = df


combined_df.to_csv(OUTPUT_FILE, index=False)


print("\n========================================")
print(" ATTACK DATASET UPDATED")
print("========================================")
print(f"New flows collected: {len(df)}")
print(f"Total SCAN flows: {len(combined_df)}")
print(f"Dataset saved to: {OUTPUT_FILE}")