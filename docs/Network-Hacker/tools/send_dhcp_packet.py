from scapy.all import *

ether_header = Ether(src="00:50:79:66:68:00", dst="ff:ff:ff:ff:ff:ff")
ip_header = IP(src="0.0.0.0", dst="255.255.255.255")
udp_header = UDP(sport=68, dport=67)
bootp_header = BOOTP(chaddr=RandString(12, "0123456789abcdef"))

request_option_1 = 1    # Subnet Mask
request_option_2 = 6    # DNS
request_option_3 = 15   # Domain Name
request_option_4 = 44   # NetBIOS (TCP/IP) Name Servers
request_option_5 = 3    # Routers
request_option_6 = 33   # Static Routes
request_option_7 = 150  # TFTP Server address
request_option_8 = 43   # Vendor Specific Information
request_option_9 = 252  # Proxy / wpad

bytes_request_options = struct.pack(b"9B", request_option_1, request_option_2, request_option_3, request_option_4, request_option_5, request_option_6, request_option_7, request_option_8, request_option_9)

dhcp_header = DHCP(options=[(b'message-type', b'discover'), (b'param_req_list', bytes_request_options), b'end'])

packet = ether_header / ip_header / udp_header / bootp_header / dhcp_header

sendp(packet, iface = "eth0")
