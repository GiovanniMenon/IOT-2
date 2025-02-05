import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSparseDataBlock
from pymodbus.server import ModbusTcpServer
from pymodbus.server import StartAsyncTcpServer, ServerAsyncStop
import time
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)


LOCAL_ADDRESS = 'localhost'

# In modbus client - server/master/main node
async def initialize_master(port):
    client = AsyncModbusTcpClient(LOCAL_ADDRESS, port=port)
    await client.connect()
    return client

# In modbus the server is the field device (sensor/servo/etc)
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
        master.close()

async def TC5(port=5030):
    await initialize_tcp_server(port)
    client = await initialize_master(port)

    try:
        while True:
            time.sleep(1)
            response = await client.read_coils(address=1, count=5)
            # response = await client.write_coil(1, False)

            # Check if the response contains errors
            if response.isError():
                print(f"Error: {response}")
            # else:
            #     print(f"Received data from slave: {int(response.bits[0])}, {response.address}, {response.bits}")
            #     # print(await client.read_coils(address=1, count=5))
    except Exception as e:
        print(f"Error communicating with slave: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    # asyncio.run(execute_irregular_tcp_framing_attack())
    asyncio.run(TC5())