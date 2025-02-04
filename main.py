import asyncio
import array
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSparseDataBlock
from pymodbus.server import ModbusTcpServer
from pymodbus.server import StartAsyncTcpServer, ServerAsyncStop

LOCAL_ADDRESS = 'localhost'

async def initialize_master(port):
    master = AsyncModbusTcpClient(LOCAL_ADDRESS, port=port)
    await master.connect()
    return master

async def initialize_tcp_server(port):
    slave = ModbusSlaveContext(co=ModbusSparseDataBlock([True] * 10))
    context = ModbusServerContext(slave, True)

    asyncio.create_task(StartAsyncTcpServer(context, address=(LOCAL_ADDRESS, port)))


async def execute_irregular_tcp_framing_attack(port=5030):
    # Initialize TCP server
    await initialize_tcp_server(port)

    # Initialize master
    master = await initialize_master(port)

    try:
        print(await master.read_coils(address=1, count=5))
        response = await master.write_coil(1, False)

        # Check if the response contains errors
        if response.isError():
            print(f"Error: {response}")
        else:
            print(f"Received data from slave: {response.address}, {response.bits}")
            print(await master.read_coils(address=1, count=5))

    except Exception as e:
        print(f"Error communicating with slave: {e}")
    finally:
        # Close the connection
        master.close()


if __name__ == "__main__":
    asyncio.run(execute_irregular_tcp_framing_attack())