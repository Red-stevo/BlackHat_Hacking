import os
import socket

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hex_dump(packet, length=16):
    if isinstance(packet, bytes):
        packet = packet.decode()

    result = list()
    for i in range(0, len(packet), length):
        word = str(packet[i:i + length])
        printable = word.translate(HEX_FILTER)
        hexa = ''.join([f'{ord(c):02x}' for c in word])
        hex_width = length * 3
        result.append(f'{i:04x} {hexa:<{hex_width}} {printable}\n\n\n')

    for line in result:
        print(line)


class Packet_Sniffer:
    def __init__(self, host_ip="0.0.0.0", host_port=0):
        self.host_ip = host_ip
        self.host_port = host_port
        self.sniffer = None

        if os.name == "nt":
            self.sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            self.sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            self.sniffer.bind((host_ip, host_port))
            self.sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        else:
            self.sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x003))

        self.receive_packets()

    def receive_packets(self):

        while True:
            hex_dump(self.sniffer.recvfrom(65565))


if __name__ == "__main__":
    Packet_Sniffer = Packet_Sniffer()
