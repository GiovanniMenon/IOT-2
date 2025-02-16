import socket
import time

LOCAL_ADDRESS = 'localhost'

PROXY_PORT = 5000 
MODBUS_SERVER_PORT = 5030

DELAY_SECONDS = 5


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((LOCAL_ADDRESS, PROXY_PORT))
# Max 5 queued connections
server_socket.listen(5)

print(f"Proxy Server listening on {LOCAL_ADDRESS}:{PROXY_PORT}")

# Listen for requests comming in to Proxy
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    data = client_socket.recv(1024)
    print(f"data received: {data}")

    # stop listening after receiving the message
    if data:
        break

# Delay the request to Modbus server
time.sleep(DELAY_SECONDS)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as modbus_socket:
    modbus_socket.connect((LOCAL_ADDRESS, MODBUS_SERVER_PORT))
    print(f"Forwarding data to Modbus server on {LOCAL_ADDRESS}:{MODBUS_SERVER_PORT}")
    
    # Send the received data to the Modbus server
    modbus_socket.sendall(data)

    # Receive response from the Modbus server
    response = modbus_socket.recv(1024)
    print(f"Received response from Modbus server: {response}")

# Delay response to the sender
time.sleep(DELAY_SECONDS)

# Send response back to the sender
client_socket.sendall(response)

# Close connections
client_socket.close()
server_socket.close()