import argparse
import socket
import textwrap


class PostScanner:
    def __init__(self, target_ip, target_port, args):
        self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
        self.target_ip = target_ip
        self.target_port = target_port
        self.args = args

    def send_packet(self):
        addr = []
        self.udp_client.sendto(b'', (self.target_ip, self.target_port))
        self.udp_client.settimeout(self.args.timeout)

        try:
            data, addr = self.udp_client.recvfrom(65565)
            print(f"Port {addr[1]} Opened")
        except Exception as e:
            print(f"Port {addr[1]} Closed.")


if __name__ == "__main__":
    terminal_arguments = argparse.ArgumentParser(
        description="Network Port Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
Examples :


_init__.py -t 10.10.10.1-255  -p 1-65565
_init__.py -t 10.10.10.1  -p 21
'''))

    terminal_arguments.add_argument('-p', '--port', required=True, help='ip(s)  to  scan. ')
    terminal_arguments.add_argument('-t', '--target', required=True, help='Target(s) to scan.')
    terminal_arguments.add_argument('-s', '--timeout', type=int, default=1, help="Specify The Timeout")

    argument = terminal_arguments.parse_args()
