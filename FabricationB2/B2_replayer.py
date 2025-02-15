import socket
import pyshark

capture_filter = "tcp.port == 5030"

# CHANGE THIS IF IT DOESN'T CORRESPOND TO THE INTERFACE FOR YOUR SYSTEM
INTERFACE = 'Adapter for loopback traffic capture'
LOCAL_ADDRESS = 'localhost'
PORT = 5030

cap = pyshark.LiveCapture(INTERFACE, display_filter=capture_filter)

payload = None

for packet in cap.sniff_continuously():
        if hasattr(packet, 'tcp') and hasattr(packet, 'Data') and hasattr(packet.Data, 'Data'):
            payload = packet.Data.Data
            print(f"Packet Data: {payload}")
            break

print("found a packet with payload")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.settimeout(60)
        sock.connect((LOCAL_ADDRESS, PORT))  # Connect to Modbus server
        print("Connected, replaying the message")

        # Convert the cleaned string (which is now a valid hex string) to bytes
        raw_payload = bytes.fromhex(payload)  # Now this is valid hex

        sock.sendall(raw_payload)  # Send the Modbus frame
        response = sock.recv(1024)  # Receive server's response
        
        print("Sent Modbus Request:", raw_payload.hex())
        print("Received Response:", response.hex())

    except Exception as e:
        print(f"Error sending Modbus request: {e}")