from scapy.all import sniff 
IP_MAC_Map = {}

def processPacket(packet):
    src_IP = packet['ARP'].psrc
    src_MAC = packet['Ether'].src
    if src_MAC in IP_MAC_Map.keys():
        if IP_MAC_Map[src_MAC] != src_IP : 
            try:
                old_IP =  IP_MAC_Map[src_MAC]
            except: 
                old_IP = "unknown"
            message = ("\n Possible ARP attack detected \n "
                        + "Involving machine with IP address \n " 
                        + str(old_IP) + " and " + str(src_IP)
                         +"\n ")
            return message
    else: 
        IP_MAC_Map[src_MAC] = src_IP

sniff(count=0, filter="arp", store = 0, prn = processPacket)