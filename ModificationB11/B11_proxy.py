import socket
import time

LOCAL_ADDRESS = 'localhost'

PROXY_PORT = 5000 
MODBUS_SERVER_PORT = 5030


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((LOCAL_ADDRESS, PROXY_PORT))
server_socket.listen(5)  # Max 5 queued connections

print(f"Proxy Server listening on {LOCAL_ADDRESS}:{PROXY_PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    data = client_socket.recv(1024)
    print(f"data received: {data}")

    if data:
        break

time.sleep(4)

print("Slept")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as modbus_socket:
    modbus_socket.connect((LOCAL_ADDRESS, MODBUS_SERVER_PORT))
    print(f"Forwarding data to Modbus server on {LOCAL_ADDRESS}:{MODBUS_SERVER_PORT}")
    
    modbus_socket.sendall(data)  # Send the received data to the Modbus server

    # Receive response from the Modbus server
    response = modbus_socket.recv(1024)
    print(f"Received response from Modbus server: {response}")

client_socket.sendall(data)  # Send response
client_socket.close()