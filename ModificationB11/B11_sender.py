import sys
import os
import socket
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from InterruptionTC5 import T5_attack as module

 # Send a write request to the Proxy to change value to True at address 0
modbus_request = module.create_modbus_request(1, 1, 5, 0, 1, True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("localhost", 5000))

    # Start a timer to check how long the sender has to wait for the response
    start_time = time.time()

    # Send message to the Proxy
    sock.sendall(modbus_request)

    # Read response
    received = sock.recv(1024)

# Calculate seconds elapsed
elapsed_time = time.time() - start_time

print("==========SENT==========")
print(modbus_request)

print("==========RECEIVED==========")
print(received)

print(f"Seconds elapsed from request sending to response receiving: {elapsed_time}")