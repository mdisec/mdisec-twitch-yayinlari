from scapy.all import * 

ether_header = Ether(src="00:11:22:33:44:88", dst="00:0c:29:18:3b:16")
ip_header = IP(dst = "10.0.40.3", src = "10.0.40.167", ttl=2)
icmp_header =  ICMP(type = 8, code = 0)
packet = ether_header / ip_header / icmp_header
ls(packet)
sendp(packet) 