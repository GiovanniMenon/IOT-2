from pymodbus.client import ModbusTcpClient
import logging


FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.disable(logging.CRITICAL)
LOCAL_ADDRESS = 'localhost'  
PORT = 5030  


def scan_address(client, slave_id):
    try:
        result = client.read_holding_registers(0, slave=slave_id)
        if not result.isError():
            return slave_id, result.registers
    except Exception:
        pass
    return None

def scan_network(host, port, start_address=1, end_address=247):
    client = ModbusTcpClient(host, port=port)
    devices_found = {}

    for slave_id in range(start_address, end_address + 1):
        result = scan_address(client, slave_id)
        if result:
            devices_found[result[0]] = result[1]

    client.close()
    return devices_found


if __name__ == "__main__":

    devices_found = scan_network(LOCAL_ADDRESS, PORT)
    
    for slave_id, registers in devices_found.items():
        print(f"Slave {slave_id} - Holding Registers: {registers}")
