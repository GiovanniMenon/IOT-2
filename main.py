import asyncio
import array
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSparseDataBlock
from pymodbus.server import ModbusTcpServer
from pymodbus.server import StartAsyncTcpServer, ServerAsyncStop

# class Master(AsyncModbusTcpClient):
#     async def __init__(self, port=5020):
#         super().__init__('localhost', port=port)
LOCAL_ADDRESS = 'localhost'


async def initialize_master(port):
    master = AsyncModbusTcpClient("localhost", port=port)
    await master.connect()
    return master

async def initialize_tcp_server(slave_count, port):
    slaves_dictionary = {}

    for i in range(slave_count):
        # Create modbus slave with holding registers, on which read/write operations can be performed
        slave = ModbusSlaveContext(hr=ModbusSparseDataBlock([i] * 3))
        slaves_dictionary[i] = slave

    context = ModbusServerContext(slaves_dictionary, False)

    print(port)

    asyncio.create_task(StartAsyncTcpServer(context, address=("localhost", port)))


async def execute_irregular_tcp_framing_attack(port=5030):
    # Initialize TCP server
    await initialize_tcp_server(3, port)

    print("Yo")
    # Initialize master
    master = await initialize_master(port)

    print(master)

    try:
        # Send a Read Holding Registers request to register 0, requesting 5 registers
        response = await master.write_coil(0, 0)

        print("Hello")
        # Check if the response contains errors
        if response.isError():
            print(f"Error: {response}")
        else:
            print(f"Received data from slave: {response.address}, {response.bits}")

    except Exception as e:
        print(f"Error communicating with slave: {e}")
    finally:
        # Close the connection
        master.close()


if __name__ == "__main__":
    asyncio.run(execute_irregular_tcp_framing_attack())