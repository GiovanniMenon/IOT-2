import socket

LOCAL_ADDRESS = 'localhost'  # Listen on all available network interfaces
PORT = 5000      # Change this to your desired port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((LOCAL_ADDRESS, PORT))
server_socket.listen(5)  # Max 5 queued connections

def create_modbus_request(transaction_id, unit_id, function_code, start_address, num_registers):
    """Construct a Modbus TCP request frame."""
    protocol_id = 0x0000  # Modbus Protocol
    length = 6  # PDU length (Function Code + Address + Quantity = 6 bytes)
    
    # Pack into bytes
    request = (
        transaction_id.to_bytes(2, byteorder='big') +
        protocol_id.to_bytes(2, byteorder='big') +
        length.to_bytes(2, byteorder='big') +
        unit_id.to_bytes(1, byteorder='big') +
        function_code.to_bytes(1, byteorder='big') +
        start_address.to_bytes(2, byteorder='big') +
        num_registers.to_bytes(2, byteorder='big')
    )
    return request

print(f"Server listening on {LOCAL_ADDRESS}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    data = client_socket.recv(1024)
    if not data:
        break
    print(f"Received: {data.decode()}")

    client_socket.sendall(b"Hello from server!")  # Send response
    client_socket.close()