from scapy.all import *
import secrets
from threading import Thread

interface = "eth0"
tid = secrets.SystemRandom().randint(0, 450000)
fam, hw = get_if_raw_hwaddr(interface)


# srcMac = '08:00:27:1f:30:76'
# srcMacB = b'\x08\x00\x27\x1f\x30\x76'
srcMac = "00:00:00:00:00:00"
# srcMacB = b'\x00\x0c\x29\x85\xe1\x63'
srcMacB = b'\xff\xff\xff\xff\xff\xff'
offerIP = "10.10.10.16"

ether = Ether(dst='ff:ff:ff:ff:ff:ff', src=srcMac, type=0x800)
ip = IP(src= '0.0.0.0', dst='255.255.255.255')
udp = UDP(sport=68, dport=67)
bootp = BOOTP(chaddr=srcMacB, ciaddr= '0.0.0.0', xid = tid, flags=1)

def discovery():
    dhcp = DHCP(options=[("message-type", "discover"), "end"])
    packet = ether/ip/udp/bootp/dhcp
    sendp(packet, iface=interface, verbose=False)
    print("D")

def offer_get ():
    global offerIP
    if DHCP in packet and packet[DHCP].options[0][1] == 2:
        offerIP = packet.getlayer[BOOTP].yiaddr
        print("Offer IP", offerIP)
        request()
        return True
    else:
        return False

def ack_get(packet):
    if DHCP in packet:
        if packet[DHCP].options[0][1] == 5:
            print("A")
            return True
        if packet[DHCP].options[0][1] == 6:
            print("N")
            return True
        return False
    else:
        return False

def offer():
    sniff(iface=interface, stop_filter=offer_get)

def ack():
    sniff(iface=interface, stop_filter=ack_get)

def request():
    dhcp = DHCP(options=[
        ("message-type", "request"),
        ("requested_addr", offerIP),
        ("hostname", "kali2"),
        ("param_req_list", [1, 28, 2, 3, 15, 6, 119, 12, 44, 47, 26, 121, 42]),
        "end"])
        packet = ether/ip/udp/bootp/dhcp

        sendp(packet, iface=interface, verbose=False)
        print("R")


def realease():
    global bootp, srcMacB
    srcMacB = b'\x00\x0c\x29\x85\xe1\x63'
    bootp = BOOTP(chaddr=srcMacB, ciaddr='10.10.10.16', xid=tid)
    dhcp = DHCP(options=[("message-type", "release"), ("requested_addr", "10.10.10.16"), "end"])
    packet = ether/ip/udp/bootp/dhcp

    sendp(packet, iface=interface, verbose=False)
    print("Realease")

dum1 = Thread(target=discovery)
dum2 = Thread(target=offer)
dum3 = Thread(target=ack)

dum1.start()
dum2.start()
dum3.start()

#realease()