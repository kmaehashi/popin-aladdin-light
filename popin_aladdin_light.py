#!/usr/bin/env python

import argparse
import collections
import json
import socket
import struct
import sys
import time


_cealing_buttons = collections.OrderedDict([
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

_projector_buttons = collections.OrderedDict([
    ('home', 35),
    ('up', 36),
    ('right', 37),
    ('down', 38),
    ('ok', 49),
    ('left', 50),
])

_projector_stateless_buttons = collections.OrderedDict([
    ('back', 48),
    ('vol_up', 115),
    ('vol_down', 114),
    ('power', 116),
    ('menu', 139),
])


_header_format = '<IBB'


def _pack(op1, op2, payload_obj):
    payload = json.dumps(payload_obj).encode('utf-8')
    header = struct.pack(_header_format, len(payload), op1, op2)
    return header + payload


def _send_tcp(host, data, null_reply=False, port=30913):
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


def _send_udp(host, data, port=16735):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(data.encode('ascii'), (host, port))
    finally:
        sock.close()


def ping_cealing(host):
    return _send_tcp(host, _pack(0, 0, 1), True)


def light(host, button):
    return _send_tcp(host, _pack(1, 7, {'action': _buttons[button]}))


def text(host, text):
    return _send_tcp(host, _pack(1, 10, {'text': text}))


def voice_control(host, text):
    return _send_tcp(host, _pack(1, 9, {'text': text, 'success': true}))


def _projector_set_key_status(host, key, state):
    _send_udp(host, 'KEYSSTATUS:{}+{}'.format(key, '1' if state else '0'))


def projector(host, button, duration=0.1):
    if button in _projector_buttons.keys():
        key = _projector_buttons[button]
        _projector_set_key_status(host, key, True)
        time.sleep(duration)

        # Note: release event for the key is sent twice.
        for other_key in _projector_buttons.values():
            _projector_set_key_status(host, other_key, False)
        _projector_set_key_status(host, key, False)
    elif button in _projector_stateless_buttons.keys():
        key = _projector_stateless_buttons[button]
        _send_udp(host, 'KEYPRESSES:{}'.format(key))
    else:
        assert False


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('--ping', default=False, action='store_true')
    parser.add_argument('--projector', type=str, default=None,
                        choices=(list(_projector_buttons.keys()) +
                                 list(_projector_stateless_buttons.keys())))
    parser.add_argument('--light', type=str, default=None,
                        choices=_cealing_buttons.keys())
    parser.add_argument('--text', type=str, default=None)
    parser.add_argument('--repeat', type=int, default=1)
    args = parser.parse_args(argv)

    for i in range(args.repeat):
        if args.ping:
            ping(args.host)
        if args.light:
            light(args.host, args.light)
        if args.projector:
            projector(args.host, args.projector)
        if args.text:
            text(args.host, args.text)

        time.sleep(0.1)


if __name__ == '__main__':
    main(sys.argv[1:])
