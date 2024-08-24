import os
import socket
import struct
import sys


def decode_packet(packet_data):
    # IP headers are usually 20 bytes long
    IP_HEADER_LENGTH = 20

    print(packet_data)

    # Unpack only if enough bytes are available for the IP header
    if len(packet_data) >= IP_HEADER_LENGTH:
        # Extract the first 20 bytes for the IP header
        ip_header = packet_data[:IP_HEADER_LENGTH]

        # Unpack IP header
        try:
            ip_header_fields = struct.unpack('!BBHHHBBH4s4s', ip_header)

            # Extract individual fields from the unpacked header
            version_and_ihl = ip_header_fields[0]
            version = version_and_ihl >> 4
            ihl = version_and_ihl & 0xF
            total_length = ip_header_fields[2]

            # Convert addresses from binary to readable format
            src_ip = socket.inet_ntoa(ip_header_fields[8])
            dst_ip = socket.inet_ntoa(ip_header_fields[9])

            print(f"Version: {version}, Header Length: {ihl * 4} bytes, Total Length: {total_length} bytes")
            print(f"Source IP: {src_ip}, Destination IP: {dst_ip}")

        except struct.error as e:
            print(f"Error unpacking IP header: {e}")
    else:
        handle_icmp_packet(packet_data)


def handle_icmp_packet(icmp_data):
    ICMP_HEADER_LENGTH = 8  # Standard length of ICMP header

    if len(icmp_data) < ICMP_HEADER_LENGTH:
        print(f"Packet too short for ICMP header: {len(icmp_data)} bytes")
        return

    # Extract the ICMP header from the packet
    icmp_header = icmp_data[:ICMP_HEADER_LENGTH]

    try:
        icmp_header_fields = struct.unpack('!BBHHH', icmp_header)

        icmp_type = icmp_header_fields[0]
        icmp_code = icmp_header_fields[1]
        icmp_checksum = icmp_header_fields[2]

        print(f"ICMP Type: {icmp_type}, Code: {icmp_code}, Checksum: {icmp_checksum}")

    except struct.error as e:
        print(f"Error unpacking ICMP header: {e}")


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

        self.sniffer_dog = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
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
        while True:
            print(self.sniffer_dog.recvfrom(65565))


def main():
    if len(sys.argv) != 3:
        print("setting default port to 0 and ip to '0.0.0.0'")
        Sniffer_dog()
    else:
        Sniffer_dog(sys.argv[1], int(sys.argv[2]))


if __name__ == "__main__":
    main()
