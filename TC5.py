import socket

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

# Two valid Modbus messages in a single TCP frame
modbus_request_1 = create_modbus_request(1, 1, 3, 0, 10)  # Read 10 registers from address 0
modbus_request_2 = create_modbus_request(2, 1, 3, 100, 5)  # Read 5 registers from address 100

# Combine both requests in a single TCP frame
combined_request = modbus_request_1 + modbus_request_2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("localhost", 5030))
    sock.sendall(combined_request)  # Send both messages together

    # Read response (assuming server can handle multiple messages in one frame)
    received = sock.recv(1024)

print("Sent:", combined_request.decode())
print("Received:", received.decode())
