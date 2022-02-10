from scapy.all import *

def processPacket(packet):
	if packet['TCP'].flags ==  'FPU':
		print("Xmas Scan Detected on Port ",packet['TCP'].dport)

sniff(iface="lo", count = 1000, filter="tcp", store=0, prn = processPacket)

