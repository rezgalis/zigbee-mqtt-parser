#!/usr/bin/python3

#for post-update script - useful if using https://github.com/rezgalis/gitPyUpdater

from subprocess import Popen, PIPE

args = ["pkill" , "-f", "zigbee-mqtt-listener.py"]
proc = Popen(args, stdout=PIPE, stderr=PIPE)
out, err = proc.communicate()
print(err)

args = ["python" , "/home/pi/zigbee-mqtt-parser/zigbee-mqtt-listener.py"]
proc = Popen(args, stdout=PIPE, stderr=PIPE)
out, err = proc.communicate()
print(err)
