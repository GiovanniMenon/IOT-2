import asyncio
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
from pymodbus.server import StartAsyncTcpServer
import logging


FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
logging.disable(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

SERVERS = [
    ("localhost", 5030, {
        1: ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [10] * 100)),
        5: ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [30] * 100)),
    }),
    ("localhost", 5020, {
        56: ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [50] * 100)),
        77: ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [70] * 100)),
    }),
    ("localhost", 5010, {
        17: ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [10] * 100)),
        59: ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [30] * 100)),
    }),
    ("localhost", 5000, {
        26: ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [50] * 100)),
        197: ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [70] * 100)),
    }),
]

async def start_server(ip, port, slaves):
    context = ModbusServerContext(slaves=slaves, single=False)
    print(f"Starting Modbus Server on {ip}:{port}")
    await StartAsyncTcpServer(context, address=(ip, port))

async def main():
    tasks = [start_server(ip, port, slaves) for ip, port, slaves in SERVERS]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
