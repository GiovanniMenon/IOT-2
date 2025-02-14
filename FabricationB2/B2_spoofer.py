import pyshark
import logging

# Set up logging for the sniffer
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def sniff_modbus_packets(interface="Loopback Pseudo-Interface 1"):
    """Sniff Modbus packets over the specified interface"""
    capture = pyshark.LiveCapture(interface=interface, display_filter="modbus")
    log.info("Sniffing Modbus packets...")
    for packet in capture.sniff_continuously():
        log.info(f"Captured packet: {packet}")
        print(packet)

# To allow it to be used as a script as well:
if __name__ == "__main__":
    sniff_modbus_packets(interface="Loopback Pseudo-Interface 1")  # Adjust the interface name if needed