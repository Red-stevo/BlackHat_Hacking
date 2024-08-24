import os
import socket
import sys


class Sniffer_dog:
    def __init__(self, host_ip="0.0.0.0", host_port=0):
        self.host_ip = host_ip
        self.host_port = host_port
        self.sniff_protocol = None
        self.sniffer_dog = None
        if os.name == "nt":
            self.sniff_protocol = socket.IPPROTO_IP
        else:
            self.sniff_protocol = socket.IPPROTO_ICMP

        self.sniffer_dog = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.sniff_protocol)
        self.sniffer_dog.bind((host_ip, host_port))

        # configuring sniffing options. allows capturing of the packet headers.
        self.sniffer_dog.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # if the os is windows we need to allow promiscuous mode to capture all packets.
        if os.name == "nt":
            self.sniffer_dog.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        self.packet_sniff()

        # Disabling the promiscuous mode if the os is windows.
        if os.name == "nt":
            self.sniffer_dog.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

    def packet_sniff(self):
        print(self.sniffer_dog.recvfrom(65565).decode('utf-8'))


def main():
    if len(sys.argv) != 3:
        print("setting default port to 0 and ip to '0.0.0.0'")
        Sniffer_dog()
    else:
        Sniffer_dog(sys.argv[1], int(sys.argv[2]))


if __name__ == "__main__":
    main()
