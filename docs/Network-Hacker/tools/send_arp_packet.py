from scapy.all import * 

ether_header = Ether(src="00:11:22:33:66:99", dst="ff:ff:ff:ff:ff:ff")
arp_header = ARP(hwsrc="00:11:22:33:66:99", psrc="10.0.40.67", hwdst="00:00:00:00:00:00", pdst="10.0.40.3", op=1)
packet = ether_header / arp_header
ls(packet)
sendp(packet) 
