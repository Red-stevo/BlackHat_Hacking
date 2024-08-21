import socket


class UDPClient:

    def __init__(self):
        self.client = None
        self.host_ip = "127.0.0.1"
        self.host_port = 80

    def send_datagram(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.sendto(b"The is a UDP datagram.", (self.host_ip, self.host_port))

        data, addr = self.client.recvfrom(4896)

        print(data, addr)


client = UDPClient()

client.send_datagram()
