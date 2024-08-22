import argparse as ps
import shlex
import subprocess
import textwrap as tw
import subprocess as sp


def main():
    parser = ps.ArgumentParser(description="Netcat tool in python",
                               formatter_class=ps.RawDescriptionHelpFormatter,
                               epilog=tw.dedent('''
        python3 __init__.py <IP> <args>
            -l  --listen 
            -u  --udp 
            -p  --port
                                     '''))

    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')

    args = parser.parse_args()


def execute(command):
    command = command.strip()
    if not command:
        print("Error.Command Not Provided.")
        return
    output = sp.check_output(shlex.split(command), stderr=subprocess.STDOUT)

    return output.decode('utf-8')


if __name__ == "__main__":
    main()

