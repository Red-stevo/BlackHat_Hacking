import socket


class Tcp_Client:
    def __init__(self):
        self.host_ip = "127.0.0.1"
        self.host_port = 1001
        self.client = None

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host_ip, self.host_port))
        self.client.send(b"GET / HTTPS/1.1\r\nHOST:google.com\r\n\r\n")
        response = self.client.recv(4896)
        print(response)
        print(response)


if __name__ == "__main__":
    client = Tcp_Client()
    client.connect()
