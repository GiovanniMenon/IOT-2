
from concurrent.futures import thread
import time
import pyshark

# Define the capture filter (only TCP traffic on port 5030)
capture_filter = "tcp.port == 5030"

# Start capturing packets using PyShark (live capture from a network interface)
cap = pyshark.LiveCapture(interface='Adapter for loopback traffic capture', display_filter=capture_filter)

# You can replace 'eth0' with the network interface you are using (e.g., 'lo0' for localhost).

# Loop through the packets and check for the specific data in the payload
for packet in cap.sniff_continuously():
    print(packet)
    # Check if the packet has a TCP layer and a Data field (payload)
    if 'TCP' in packet:
        # Check the payload to see if it contains the target data (in hexadecimal)
        if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'payload'):
            payload = packet.tcp.payload
            print(f"Found target data in packet: {packet}")
            print(f"Packet Data: {payload}")

            # src_ip = packet.ip.src
            # src_port = int(packet.tcp.srcport)
            # # Send the captured packet to the Modbus server using Scapy
            # try:
            #     # Construct the IP and TCP layers with the payload (raw Modbus request)
            #     ip = IP(src=src_ip, dst=modbus_host)
            #     tcp = TCP(sport=src_port, dport=modbus_port, flags="A", seq=random.randint(1, 1000), ack=random.randint(1, 1000))

            #     # Resend the Modbus TCP packet using the captured payload
            #     pkt = ip/tcp/Raw(load=payload)
            #     send(pkt)
            #     print(f"Packet resent to {modbus_host}:{modbus_port}")
            
            # except Exception as e:
            #     print(f"Failed to send Modbus packet: {e}")
    time.sleep(10)