import socket
import threading


def client_handler(client_soket):
    with client_soket as sok:
        request = sok.recv(1024)
        print(f"Received : {request.decode('utf-8')}")
        sok.send(b"ACK")


class TCPServer:
    def __init__(self):
        self.IP = "0.0.0.0"  # listen on all interfaces.
        self.PORT = 1001
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen()

    def listen(self):
        self.server.bind((self.IP, self.PORT))
        self.server.listen(3)

        while True:
            client, addr = self.server.accept()
            print(f"[*] Connected to : {addr[0]}:{addr[1]}")

            handler = threading.Thread(target=client_handler, args=(client,))
            handler.start()


if __name__ == "__main__":
    TCPServer = TCPServer()
