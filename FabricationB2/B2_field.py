import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSparseDataBlock
from pymodbus.server import StartAsyncTcpServer
import logging
import random

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

LOCAL_ADDRESS = 'localhost'
PORT = 5030

def update_sensor(context):
    """After the master read the sensor register we change his stored number with a random one"""
    value = random.randint(0, 100)  
    context[0].setValues(3, 0, [value])  
    log.info(f"Sensor value updated: {value}")

async def master_task(host, port, interval, context):
    """
    Master initialization
 
    Interval: interval between each read
    Context: field device context to call the update_sensor function
    """
    client = AsyncModbusTcpClient(host=host, port=port)
    await client.connect()
    
    while True:
        rr = await client.read_holding_registers(address=0, count=1, slave=1) 
        if not rr.isError():
            log.info(f"Master read value: {rr.registers}")
            update_sensor(context)
        else:
            log.error(f"Read error: {rr}")
        await asyncio.sleep(interval)

async def main():

    slave = ModbusSlaveContext(co=ModbusSparseDataBlock([10])) 
    context = ModbusServerContext(slave, single=True)
    
    server_task = asyncio.create_task(StartAsyncTcpServer(context, address=(LOCAL_ADDRESS, PORT)))
    master_task_instance = asyncio.create_task(master_task(LOCAL_ADDRESS, PORT, 10, context))
    
    await asyncio.gather(server_task, master_task_instance)

if __name__ == "__main__":
    """
    The scenario here is a normal CLIENT/SERVER communication.
    Attacker aim to change each time the new Client value by replayng old traffic sent by the SERVER (containing past information). 
    (Just a possible application)
    """
    asyncio.run(main())