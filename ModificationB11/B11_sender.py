import asyncio
import sys
import os
import socket

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from InterruptionTC5 import T5_attack as module

 # Two valid Modbus messages in a single TCP frame
modbus_request = module.create_modbus_request(1, 1, 1, 0, 1)  # Read 10 registers from address 0

print(modbus_request)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("localhost", 5000))
    sock.sendall(modbus_request)  # Send both messages together

    # Read response (assuming server can handle multiple messages in one frame)
    received = sock.recv(1024)
print("==========SENT==========")
module.parse_modbus_response(modbus_request)
print("==========RECEIVED==========")
module.parse_modbus_response(received)


