# -*- coding: utf-8 -*-
import sys
import argparse

import socket_request

import json
from devtools import debug
try:
    from .__version__ import __version__
except:
    from __version__ import __version__
import time


def get_parser():
    parser = argparse.ArgumentParser(
        description='Command Line Interface for control_chain',
        fromfile_prefix_chars='@'
    )
    parser.add_argument(
        'command',
        choices=['start', 'stop', 'reset', 'leave', 'view_chain', 'join', 'import_icon', 'backup', 'restore', 'ls'],
        help='')
    parser.add_argument('-s', '--unixsocket', metavar='unixsocket', help='unix domain socket path (default: /app/goloop/data/cli.socket)',
                        default="/app/goloop/data/cli.sock")

    parser.add_argument('-d', '--debug', action='store_true', help=f'debug mode. (default: False)', default=False)
    parser.add_argument('-t', '--timeout', metavar='timeout', help=f'timeout (default: 5)', default=5)
    parser.add_argument('-w', '--wait_state', metavar='wait_state', help=f'wait_state (default: True)', default=True)
    parser.add_argument('-ap', '--auto_prepare', metavar='auto_prepare', help=f'auto_prepare (default: True)', default=True)

    parser.add_argument('-p', '--payload', metavar='payload file', help=f'payload file', type=argparse.FileType('r'), default=None)
    parser.add_argument('-f', '--forever', action='store_true',  help=f'retry forever', default=False)
    parser.add_argument('-i', '--inspect', action='store_true',  help=f'inspect for view chain', default=False)
    return parser.parse_args()


def print_banner():
    text = """
    ╋╋╋╋╋╋╋╋╋┏┓╋╋╋╋╋┏┓╋╋╋╋┏┓
    ╋╋╋╋╋╋╋╋┏┛┗┓╋╋╋╋┃┃╋╋╋╋┃┃
    ┏━━┳━━┳━╋┓┏╋━┳━━┫┃╋┏━━┫┗━┳━━┳┳━┓
    ┃┏━┫┏┓┃┏┓┫┃┃┏┫┏┓┃┃╋┃┏━┫┏┓┃┏┓┣┫┏┓┓
    ┃┗━┫┗┛┃┃┃┃┗┫┃┃┗┛┃┗┓┃┗━┫┃┃┃┏┓┃┃┃┃┃
    ┗━━┻━━┻┛┗┻━┻┛┗━━┻━┛┗━━┻┛┗┻┛┗┻┻┛┗┛    
    """
    print(text)
    print(f"\t version : {__version__} \n\n")


def check_required(command=None):
    required_params = {
        "payload": ["import_icon"],
        "inspect": ["view_chain"]
    }

    required_keys = []

    for required_key, required_cmd in required_params.items():
        if command in required_cmd:
            required_keys.append(required_key)

    return required_keys


def main():
    print_banner()
    args = get_parser()
    if args.debug:
        print(args)

    payload = None
    inspect = None
    result = None

    if args.command == "import_icon" and args.payload is None:
        args.payload = open("/app/goloop/config/import_config.json")

    if args.payload:
        json_data = args.payload.read()
        try:
            payload = json.loads(json_data)
        except Exception as e:
            raise Exception(f"Invalid JSON - {e}")

    cc = socket_request.ControlChain(
        unix_socket=args.unixsocket,
        # cid=cid,
        debug=args.debug,
        auto_prepare=args.auto_prepare,
        wait_state=args.wait_state,
        timeout=args.timeout
        # increase_sec=2
    )
    # if args.command == "ls":
    #     args.command = "view_chain"
    #     inspect = True
    #     view_table = True

    func = getattr(cc, args.command)
    required_keys = check_required(args.command)

    if required_keys:
        arguments = {}
        for func_arg in required_keys:
            if locals().get(func_arg):
                arguments[func_arg] = locals()[func_arg]

        if args.debug:
            debug(required_keys)
            debug(arguments)

        if len(arguments) > 0:
            result = func(**arguments)
        else:
            result = func()
    else:
        result = func()

    if result and result.status_code != 200:
        socket_request.color_print(f"[ERROR] {args.command}, {result.text}", "FAIL")
    else:
        while True:
            if result:
                socket_request.color_print(f"{result.text}")
            else:
                print(cc.view_chain())

            if args.forever is False:
                sys.exit()
            time.sleep(0.2)


if __name__ == "__main__":
    sys.exit(main())
