#!/usr/bin/python3
#for post-update script - useful if using https://github.com/rezgalis/gitPyUpdater

import subprocess

subprocess.call(['pkill', '-f', 'zigbee-mqtt-listener.py'])
subprocess.call('python /home/pi/zigbee-mqtt-parser/zigbee-mqtt-listener.py&', shell=True)
