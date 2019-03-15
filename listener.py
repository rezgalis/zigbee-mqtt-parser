
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, struct, json, configparser
import paho.mqtt.client as mqtt
from datetime import datetime
from influxdb import InfluxDBClient

basepath = '/home/pi/zigbee-mqtt-parser/'

config = configparser.ConfigParser()
config.read(basepath + 'default.config')

topics_to_Grafana = ["temp", "smoke1", "smoke2"] #in zigbee2mqtt/ channel

client = InfluxDBClient(config['DEFAULT']['influx_host'], config['DEFAULT']['influx_port'], config['DEFAULT']['influx_user'], config['DEFAULT']['influx_pass'], config['DEFAULT']['influx_db'])
json_body = []


def on_message(mqttc, obj, msg):
        sensor = str(msg.topic.split("/")[1])
        #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        if sensor in topics_to_Grafana:
                message = json.loads(msg.payload)
                if sensor == "temp":
                        print("humidity: " + str(message['humidity']))
                        print("temp: " + str(message['temperature']))
                        print("battery: " + str(message['battery']))
                elif sensor == "smoke1" or sensor == "smoke2":
                        print("smoke: " + str(message['smoke']))
                        print("battery: " + str(message['battery']))
#receive message, send it only if prev notification for sensor was more than 30sec ago

#def write_Grafana():
        #json_body = [{"measurement": "zigbee","tags": {"sensor": "temp"},"fields": {"value": 0}}]
        #"time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        #client.write_points(json_body)


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.connect("localhost", 1883, 60)
mqttc.subscribe("zigbee2mqtt/#", 0)

mqttc.loop_forever()
