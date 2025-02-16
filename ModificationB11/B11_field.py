import asyncio
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSparseDataBlock
from pymodbus.server import StartAsyncTcpServer
import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')

logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
LOCAL_ADDRESS = 'localhost'

# Initialize the TCP server
async def initialize_tcp_server(port):
    slave = ModbusSlaveContext(co=ModbusSparseDataBlock([True] * 50))
    context = ModbusServerContext(slave, True)
    asyncio.create_task(StartAsyncTcpServer(context, address=(LOCAL_ADDRESS, port)))


async def server_idle(port=5030):
    await initialize_tcp_server(port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(server_idle())