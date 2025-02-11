from pymodbus.client import ModbusTcpClient

import logging
logging.disable(logging.CRITICAL)


client = ModbusTcpClient("localhost", port=5030)
devices_found = {}

# In Modbus TCP ID Address is 8bit field but from 248-255 are reserved.
# We scan all possible address to find slave field device data
for slave_id in range(1, 247):
    try:
        result = client.read_holding_registers(0, slave=slave_id)
        devices_found[slave_id] = result.registers
    except :
        pass
        
for slave_id, registers in devices_found.items():
    print(f"Slave {slave_id} - Holding Registers: {registers}")
client.close()
