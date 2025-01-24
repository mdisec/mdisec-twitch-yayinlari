from scapy.all import * 

ether_header = Ether(src="99:99:99:99:99:00", dst="ff:ff:ff:ff:ff:ff")
ip_header = IP(dst = "10.0.40.3", src = "10.0.40.100", ttl=3)
icmp_header =  ICMP(type = 8, code = 0)
packet = ether_header / ip_header / icmp_header
ls(packet)
sendp(packet) 