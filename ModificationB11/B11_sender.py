import sys
import os
import socket
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from InterruptionTC5 import T5_attack as module

 # Two valid Modbus messages in a single TCP frame
modbus_request = module.create_modbus_request(1, 1, 5, 0, 1, True)

print(modbus_request)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("localhost", 5000))

    # Start a timer to check how long the sender has to wait for the response
    start_time = time.time()
    
    # Send message to the Proxy
    sock.sendall(modbus_request)

    # Read response (assuming server can handle multiple messages in one frame)
    received = sock.recv(1024)

# Calculate seconds elapsed
elapsed_time = time.time() - start_time

print("==========SENT==========")
print(modbus_request)

print("==========RECEIVED==========")
print(received)

print(f"Seconds elapsed from request sending to response receiving: {elapsed_time}")