import asyncio
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
from pymodbus.server import StartAsyncTcpServer
import logging


FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

LOCAL_ADDRESS = 'localhost'  
PORT = 5030  


def get_context():
    slaves = {
        1: ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * 100),
            co=ModbusSequentialDataBlock(0, [0] * 100),
            hr=ModbusSequentialDataBlock(0, [10] * 100), 
            ir=ModbusSequentialDataBlock(0, [20] * 100), 
        ),
        5: ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * 100),
            co=ModbusSequentialDataBlock(0, [0] * 100),
            hr=ModbusSequentialDataBlock(0, [30] * 100),
            ir=ModbusSequentialDataBlock(0, [40] * 100),
        ),
        56: ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * 100),
            co=ModbusSequentialDataBlock(0, [0] * 100),
            hr=ModbusSequentialDataBlock(0, [50] * 100),
            ir=ModbusSequentialDataBlock(0, [60] * 100),
        ),
        77: ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * 100),
            co=ModbusSequentialDataBlock(0, [0] * 100),
            hr=ModbusSequentialDataBlock(0, [70] * 100),
            ir=ModbusSequentialDataBlock(0, [80] * 100),
        ),
        190: ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * 100),
            co=ModbusSequentialDataBlock(0, [0] * 100),
            hr=ModbusSequentialDataBlock(0, [90] * 100),
            ir=ModbusSequentialDataBlock(0, [10] * 100),
        ),
    }
    return ModbusServerContext(slaves=slaves, single=False)


async def run_server():
    context = get_context()
    await StartAsyncTcpServer(context, address=(LOCAL_ADDRESS, PORT))

if __name__ == "__main__":
    asyncio.run(run_server())
