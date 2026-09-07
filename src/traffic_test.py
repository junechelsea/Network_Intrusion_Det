from scapy.all import sniff

print("Starting packet capture...")
print("Capturing 10 packets...\n")

packets = sniff(count=10)

print("\nCapture complete!")
print(f"Packets captured: {len(packets)}\n")

for i, packet in enumerate(packets, start=1):
    print(f"--- Packet {i} ---")
    packet.show()