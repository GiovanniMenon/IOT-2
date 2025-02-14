import pyshark
import logging

# Set up logging for the sniffer
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def sniff_modbus_packets(interface="Adapter for loopback traffic capture"):
    """Sniff Modbus packets over the specified interface"""
    capture = pyshark.LiveCapture(interface=interface)
    log.info("Sniffing Modbus packets...")
    packet_count = 0
    for packet in capture.sniff_continuously():  # Limit to 10 packets for testing
        log.info(f"Captured packet: {packet}")
        # Check if the packet has a TCP layer and whether it has a Raw layer
        print(packet)

# To allow it to be used as a script as well:
if __name__ == "__main__":
    sniff_modbus_packets()
