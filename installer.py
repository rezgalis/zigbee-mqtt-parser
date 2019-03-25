#!/usr/bin/python3
#for post-update script - useful if using https://github.com/rezgalis/gitPyUpdater

import subprocess

subprocess.Popen(['pkill', '-f', 'zigbee-mqtt-listener.py'], close_fds=True)
subprocess.Popen(['python', '/home/pi/zigbee-mqtt-parser/zigbee-mqtt-listener.py'], close_fds=True)

