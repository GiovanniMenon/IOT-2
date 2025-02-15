import asyncio
from pymodbus.client import AsyncModbusTcpClient

async def send_modbus_request():
    """Connects to Modbus server and sends a request."""
    client = AsyncModbusTcpClient("localhost", port=5030)
    await client.connect()

    if client.connected:
        # Read 10 coils starting at address 0
        response = await client.read_coils(address=0, count=1, slave=1)
        
        if response.isError():
            print("Modbus Error:", response)
        else:
            print("Received Coils:", response.bits)

    client.close()

# Run the async client
asyncio.run(send_modbus_request())


