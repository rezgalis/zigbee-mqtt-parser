#!/usr/bin/python3
#for post-update script - useful if using https://github.com/rezgalis/gitPyUpdater

import os

os.system("pkill -f zigbee-mqtt-listener.py")
os.system("python /home/pi/zigbee-mqtt-parser/zigbee-mqtt-listener.py&")

