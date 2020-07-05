#!/usr/bin/python

import argparse
import collections
import json
import socket
import struct
import sys
import time


_buttons = collections.OrderedDict([
    ('switch', 31),
    ('brighter', 32),
    ('darker', 33),
    ('cooler', 34),
    ('warmer', 35),
    ('full', 36),
    ('night', 37),
    ('on', 38),
    ('off', 39),
    ('eco', 40),
    ('sleep', 41),
])


_header_format = '<IBB'


def _pack(op1, op2, payload_obj):
    payload = json.dumps(payload_obj).encode('utf-8')
    header = struct.pack(_header_format, len(payload), op1, op2)
    return header + payload


def _send(host, port, data, null_reply=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        sock.sendall(data)
        if null_reply:
            header = sock.recv(6)
            payload_len, op1, op2 = struct.unpack(_header_format, header)
            assert payload_len == 0
            assert op1 == 0
            assert op2 == 0
    finally:
        sock.close()


def ping(host, port):
    return _send(host, port, _pack(0, 0, 1), True)


def light(host, port, button):
    return _send(host, port, _pack(1, 7, {'action': _buttons[button]}))


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('--port', type=int, default=30913)
    parser.add_argument('--ping', default=False, action='store_true')
    parser.add_argument('--light', type=str, default=None,
                        choices=_buttons.keys())
    parser.add_argument('--repeat', type=int, default=1)
    args = parser.parse_args(argv)

    for i in range(args.repeat):
        if args.ping:
            ping(args.host, args.port)
        if args.light:
            light(args.host, args.port, args.light)
        time.sleep(0.1)


if __name__ == '__main__':
    main(sys.argv[1:])
