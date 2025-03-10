#!/usr/bin/env python3
# coding=utf-8
"""
  fritzbox_power_consumption - A munin plugin for Linux to monitor AVM Fritzbox
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Add the following section to your munin-node's plugin configuration:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.FRITZ_PASSWORD [fritzbox password]
  env.FRITZ_USERNAME [optional: fritzbox username]
  
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""
import json
import os
import sys

import fritzbox_helper as fh

PAGE = 'energy'
DEVICES = ['system', 'cpu', 'wifi', 'dsl', 'ab', 'usb']


def get_power_consumption():
    """get the current power consumption usage"""

    server = os.getenv('fritzbox_ip')
    password = os.getenv('FRITZ_PASSWORD')

    if "FRITZ_USERNAME" in os.environ:
        fritzuser = os.getenv('FRITZ_USERNAME')
        session_id = fh.get_session_id(server, password, fritzuser)
    else:
        session_id = fh.get_session_id(server, password)
    xhr_data = fh.get_xhr_content(server, session_id, PAGE)
    data = json.loads(xhr_data)
    devices = data['data']['drain']
    for i, device in enumerate(DEVICES):
        print('%s.value %s' % (device, devices[i]['actPerc']))


def print_config():
    if os.environ.get('host_name'):
        print("host_name " + os.getenv('host_name'))
        print("graph_title Power consumption")
    else:
        print("graph_title AVM Fritz!Box Power Consumption")
    print("graph_vlabel %")
    print("graph_category sensors")
    print("graph_order system cpu wifi dsl ab usb")
    print("system.label system")
    print("system.type GAUGE")
    print("system.graph LINE12")
    print("system.min 0")
    print("system.max 100")
    print("system.info Fritzbox overall power consumption")
    print("cpu.label cpu")
    print("cpu.type GAUGE")
    print("cpu.graph LINE1")
    print("cpu.min 0")
    print("cpu.max 100")
    print("cpu.info Fritzbox central processor power consumption")
    print("wifi.label wifi")
    print("wifi.type GAUGE")
    print("wifi.graph LINE1")
    print("wifi.min 0")
    print("wifi.max 100")
    print("wifi.info Fritzbox wifi power consumption")
    print("dsl.label dsl")
    print("dsl.type GAUGE")
    print("dsl.graph LINE1")
    print("dsl.min 0")
    print("dsl.max 100")
    print("dsl.info Fritzbox dsl power consumption")
    print("ab.label ab")
    print("ab.type GAUGE")
    print("ab.graph LINE1")
    print("ab.min 0")
    print("ab.max 100")
    print("ab.info Fritzbox analog phone ports power consumption")
    print("usb.label usb")
    print("usb.type GAUGE")
    print("usb.graph LINE1")
    print("usb.min 0")
    print("usb.max 100")
    print("usb.info Fritzbox usb devices power consumption")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
        print('yes')
    elif len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == 'fetch':
        # Some docs say it'll be called with fetch, some say no arg at all
        try:
            get_power_consumption()
        except Exception as e:
            sys.exit(f"Couldn't retrieve fritzbox power consumption: {e}")
