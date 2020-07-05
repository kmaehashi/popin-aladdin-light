#!/usr/bin/env python

import time

import popin_aladdin_light as popin


PIA_HOST = '192.168.22.111'

def projector_screen_off():
    popin.projector(PIA_HOST, 'power')
    time.sleep(0.3)
    popin.projector(PIA_HOST, 'left')
    time.sleep(0.3)
    popin.projector(PIA_HOST, 'left')
    time.sleep(0.3)
    popin.projector(PIA_HOST, 'ok')


projector_screen_off()
