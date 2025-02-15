from concurrent.futures import thread
import socket
import pyshark

capture_filter = "tcp.port == 5030"

cap = pyshark.LiveCapture(interface='Adapter for loopback traffic capture', display_filter=capture_filter)

payload = None

for packet in cap.sniff_continuously():
    if 'Data' in packet:
        if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'payload'):
            payload = packet.Data.Data
            print(f"Packet Data: {payload}")

            break

print("found a packet with payload")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # try:
        sock.settimeout(60)
        sock.connect(("localhost", 5030))  # Connect to Modbus server
        print("Connected, replaying the message")
        print(type(payload))
                
        # Convert the cleaned string (which is now a valid hex string) to bytes
        raw_payload = bytes.fromhex(payload)  # Now this is valid hex

        print(type(raw_payload))
        sock.sendall(raw_payload)  # Send invalid Modbus frame
        response = sock.recv(1024)  # Receive server's response
        
        print("Sent Malformed Request:", raw_payload.hex())
        print("Received Response:", response.hex())

    # except Exception as e:
    #     print(f"Error sending malformed Modbus request: {e}")