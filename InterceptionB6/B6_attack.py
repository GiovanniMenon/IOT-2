import logging
import socket


FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
logging.disable(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
NETWORKS = [("localhost", 5030), ("localhost", 5000), ("localhost", 5010), ("localhost", 5020)]

# @Taut Function
def create_modbus_request(transaction_id, unit_id, function_code, start_address, num_registers):
    """Construct a Modbus TCP request frame."""
    protocol_id = 0x0000  
    length = 6  
    
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

def scan_address(host, port, slave_id, start_address, num_registers):
    """Scan a single Server (Field-device) and read his holding register"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.settimeout(60)
            sock.connect((host, port))  
            request = create_modbus_request(1, slave_id, 0x03, start_address, num_registers)
            sock.send(request)  
            response = sock.recv(1024)
            
            return parse_modbus_response(response)
        
        except Exception as e:
            print(f"Error sending malformed Modbus request: {e}")



def scan_network(servers, start_address=1, end_address=247, start_register=0, num_registers=1):
    """Scan network looking for possible Server (Field-Devices)"""
    devices_found = {}

    for host, port in servers:
        for slave_id in range(start_address, end_address + 1):
            registers = scan_address(host, port, slave_id, start_register, num_registers)
            if registers:
                devices_found[(host, port, slave_id)] = registers

    return devices_found


# @Taut Function (small changes for saving parsed_data)
def parse_modbus_response(response):
    """Parses a Modbus TCP response and prints human-readable details."""
    index = 0
    parsed_data = []

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
        # print(f"\n🔹 **Modbus Frame {transaction_id}:**")
        # print(f"   - Transaction ID: {transaction_id}")
        # print(f"   - Protocol ID: {protocol_id} (Should be 0 for Modbus)")
        # print(f"   - Length: {length} bytes")
        # print(f"   - Unit ID (Slave Address): {unit_id}")
        # print(f"   - Function Code: {function_code}")

        # Interpret the response based on the function code
        if function_code == 3:  # Read Holding Registers
            registers = [int.from_bytes(data[i:i+2], byteorder='big') for i in range(0, len(data), 2)]
            print(f"   - Register Values: {registers}")
            parsed_data = registers
        # else:
        #     print(f"   - Raw Data: {data.hex()} (Unknown function code {function_code})")

        # Move to next frame in case multiple responses exist in a single TCP response
        index += 6 + length  # MBAP Header (6 bytes) + Data length

    return parsed_data

if __name__ == "__main__":
    """
    For reproducibility purposes, the various servers (field devices) were hosted on different ports and not on different ip addresses. 
    In a real application case, the hostname list is obtained by scanning the network and the port remains 502 (IANA Standard for Modbus)
    """
    print("Scanning....")
    devices_found = scan_network(NETWORKS)
    print("\n--------------|Result|--------------\nAddress\t\tID\tHolding Registers\n")
    for (host, port, slave_id), registers in devices_found.items():
        print(f"{host}:{port}\t{slave_id}\t{registers}")






        

 




