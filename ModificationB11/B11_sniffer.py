from scapy.all import *
from scapy.layers.inet import TCP

# This function is called for each packet captured
def drop_packet(pkt):
    # Check if the packet has a TCP layer
    if pkt.haslayer(TCP):
        # Check if the destination port is 5030
        if pkt[TCP].dport == 5030:
            print(f"Dropped packet: {pkt.summary()}")  # Optional: Print dropped packet summary
            return None  # Dropping the packet by returning None
    return pkt  # Return the packet if it doesn't match the condition

# BPF filter to capture only TCP packets with destination port 5030
bpf_filter = "tcp and dst port 5030"  # This will filter out packets with destination port 5030

# Start sniffing on the loopback interface and apply the filter
sniff(iface="\\Device\\NPF_Loopback", prn=drop_packet, store=0, filter=bpf_filter)