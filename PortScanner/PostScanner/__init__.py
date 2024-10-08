import argparse
import logging
import socket
import sys
import textwrap


class PostScanner:
    def __init__(self, target_ip, target_port, timeout):
        self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.target_ip = target_ip
        self.target_port = target_port
        self.timeout = timeout
        self.udp_client.settimeout(self.timeout)
        self.send_packet()

    def send_packet(self):
        addr = []
        self.udp_client.sendto(b'ACK', (self.target_ip, self.target_port))

        try:
            data, addr = self.udp_client.recvfrom(65565)
            print(f"Port {addr[1]} Opened")
        except Exception as e:
            print(f" Port : {self.target_port} Closed")


def process_hosts(passed_address):
    # Two varieties of ip addresses that can be entered.
    # 192.168.1.20
    # 192.168.1.1-255
    passed_address.strip()
    str_ip = ""

    ip_list = passed_address.split('-')

    if len(ip_list) > 2:
        logging.error("Invalid ip range.")
        sys.exit(2)

    const_ip = ip_list[0].split('.')

    for num in const_ip[:-1]:
        str_ip = f"{str_ip}{num}."

    try:
        if len(ip_list) == 1:
            return [int(const_ip[-1]), int(const_ip[-1]), str_ip]
        return [int(const_ip[-1]), int(ip_list[-1]), str_ip]
    except Exception as e:
        logging.error("Invalid ip range.", e.with_traceback())
        sys.exit(2)


def process_ports(passed_port):
    ports = passed_port.split('-')

    if len(ports) > 2:
        logging.error("Invalid port range.")
        sys.exit(3)

    try:
        return [int(ports[0]), int(ports[-1])]
    except Exception as e:
        logging.error("Invalid port range.", e)
        sys.exit(3)


def main(passed_address, passed_port, passes_timeout):
    # process the targets
    target_range = process_hosts(passed_address)

    # process the ports
    ports_range = process_ports(passed_port)

    for target in range(target_range[0], target_range[1] + 1):
        print(f"TARGET {target_range[2]}{target}")
        for port in range(ports_range[0], ports_range[1] + 1):
            scanner = PostScanner(f"{target_range[2]}{target}", port, passes_timeout)


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

    arguments = terminal_arguments.parse_args()
    try:
        main(arguments.target, arguments.port, int(arguments.timeout))
    except KeyboardInterrupt as k:
        logging.log("Exiting...")
