from scapy.all import ARP, Ether, srp

def scan_network(ip_range):

    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients.append(client_dict)
    
    return clients

def print_results(clients):
    print("Ağdaki Cihazlar:")
    print("IP Adresi\t\tMAC Adresi")
    print("-----------------------------------------")
    for client in clients:
        print(f"{client['ip']}\t\t{client['mac']}")

if __name__ == "__main__":
    ip_range = input("Tarama yapılacak IP aralığını girin: ")  
    clients = scan_network(ip_range)
    print_results(clients)
     