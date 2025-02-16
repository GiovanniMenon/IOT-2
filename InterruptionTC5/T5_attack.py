import socket

def parse_modbus_response(response):
    """Parses a Modbus TCP response and prints human-readable details."""
    index = 0
    while index < len(response):
        if len(response) - index < 7:  # Minimum valid Modbus TCP response size
            print(f"Warning: Incomplete frame detected at index {index}")
            break

        # Extract MBAP Header (7 bytes)
        transaction_id = int.from_bytes(response[index:index+2], byteorder='big')
        protocol_id = int.from_bytes(response[index+2:index+4], byteorder='big')
        length = int.from_bytes(response[index+4:index+6], byteorder='big')
        unit_id = response[index+6]
        
        # Ensure we have enough bytes for the full message
        if len(response) - index < 6 + length:
            print(f"Warning: Incomplete Modbus message at index {index}")
            break

        # Extract PDU (Function Code + Data)
        function_code = response[index+7]
        data = response[index+8: index+6+length]  # PDU Data section

        # Print the extracted information
        print(f"\n🔹 **Modbus Frame {transaction_id}:**")
        print(f"   - Transaction ID: {transaction_id}")
        print(f"   - Protocol ID: {protocol_id} (Should be 0 for Modbus)")
        print(f"   - Length: {length} bytes")
        print(f"   - Unit ID (Slave Address): {unit_id}")
        print(f"   - Function Code: {function_code}")

        # Interpret the response based on the function code
        if function_code == 3:  # Read Holding Registers
            registers = [int.from_bytes(data[i:i+2], byteorder='big') for i in range(0, len(data), 2)]
            print(f"   - Register Values: {registers}")

        elif function_code == 1:  # Read Coils
            coil_count = len(data) * 8  # Each byte contains 8 coils
            coil_values = [bool((data[i // 8] >> (i % 8)) & 0x01) for i in range(coil_count)]
            print(f"   - Coil Values: {coil_values}")

        elif function_code in [5, 6]:  # Write Single Coil or Register
            address = int.from_bytes(data[:2], byteorder='big')
            value = int.from_bytes(data[2:4], byteorder='big')
            print(f"   - Address: {address}")
            print(f"   - Written Value: {value}")

        else:
            print(f"   - Raw Data: {data.hex()} (Unknown function code {function_code})")

        # Move to next frame in case multiple responses exist in a single TCP response
        index += 6 + length  # MBAP Header (6 bytes) + Data length

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

def send_two_modbus_messages():
    # Two valid Modbus messages in a single TCP frame
    modbus_request_1 = create_modbus_request(1, 1, 1, 0, 1)  # Read 10 registers from address 0
    modbus_request_2 = create_modbus_request(2, 1, 1, 100, 5)  # Read 5 registers from address 100

    # Combine both requests in a single TCP frame
    combined_request = modbus_request_1 + modbus_request_2

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("localhost", 5030))
        sock.sendall(combined_request)  # Send both messages together

        # Read response (assuming server can handle multiple messages in one frame)
        received = sock.recv(1024)
    print("==========SENT==========")
    parse_modbus_response(combined_request)
    print("==========RECEIVED==========")
    parse_modbus_response(received)

def send_malformed_modbus_request():
    """Sends a malformed Modbus TCP frame to test the server's error handling."""
    
    # Malformed Frame 1: Incorrect Length Field (MBAP header says 6 but sends less)
    malformed_request_1 = (
        b"\x00\x01"  # Transaction ID (2 bytes)
        b"\x00\x00"  # Protocol ID (2 bytes, always 0 for Modbus)
        b"\x00\x06"  # Length (2 bytes) - Says 6 but we send less!
        b"\x01"      # Unit ID (1 byte, valid slave ID)
        b"\x03"      # Function Code (1 byte, Read Holding Registers)
        b"\x00"      # Start Address (1st byte only, missing second byte!)
    )

    # Malformed Frame 2: Invalid Function Code
    malformed_request_2 = (
        b"\x00\x02"  # Transaction ID
        b"\x00\x00"  # Protocol ID
        b"\x00\x06"  # Length
        b"\x01"      # Unit ID
        b"\xFF"      # Invalid Function Code (0xFF is not a valid Modbus function)
        b"\x00\x00"  # Start Address
        b"\x00\x05"  # Number of Registers
    )

    # Malformed Frame 3: Random Junk Data
    malformed_request_3 = b"\x00\x03\x00\x00\x00\x06\x01\x03\xDE\xAD\xBE\xEF"  # Contains garbage values

    # Combine into a single TCP frame (simulating multiple requests in one)
    combined_malformed_requests = malformed_request_1 + malformed_request_2 + malformed_request_3

    # Send to Modbus server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.settimeout(60)
            sock.connect(("localhost", 5030))  # Connect to Modbus server
            print("Connected, sending malformed request")
            sock.sendall(combined_malformed_requests)  # Send invalid Modbus frame
            response = sock.recv(1024)  # Receive server's response
            
            print("Sent Malformed Request:", combined_malformed_requests.hex())
            print("Received Response:", response.hex())

        except Exception as e:
            print(f"Error sending malformed Modbus request: {e}")
            
if __name__ == "__main__":
    send_two_modbus_messages()
    send_malformed_modbus_request()
