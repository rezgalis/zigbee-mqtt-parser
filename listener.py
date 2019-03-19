
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, struct, json, configparser
import paho.mqtt.client as mqtt
from datetime import datetime
from influxdb import InfluxDBClient

basepath = '/home/pi/zigbee-mqtt-parser/'

config = configparser.ConfigParser()
config.read(basepath + 'default.config')

topics_to_influx = ["temp", "smoke1", "smoke2"] #in zigbee2mqtt/ channel

client = InfluxDBClient(config['DEFAULT']['influx_host'], config['DEFAULT']['influx_port'], config['DEFAULT']['influx_user'], config['DEFAULT']['influx_pass'], config['DEFAULT']['influx_db'])


def is_update_time(sensor):
        should_run_update = True
	try:
		f = open(basepath + sensor +'.lastupdate', 'r')
		timestamp = int(float(f.readline()))
		prev_time = datetime.fromtimestamp(timestamp)
		f.close()
		diff = datetime.now() - prev_time
		if diff.seconds<30:
                        should_run_update = False
	except Exception:
		 pass
	return should_run_update


def write_last_log(sensor):
	f = open(basepath + sensor +'.lastupdate', 'w')
	f.write(str(time.time()))
        f.close()

        
def post_influx(json_body):
        #"time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        client.write_points(json_body)
        
        
def on_message(mqttc, obj, msg):
        sensor = str(msg.topic.split("/")[1])
        #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        if sensor in topics_to_influx and is_update_time(sensor):
                message = json.loads(msg.payload)
                data = {}
                data['measurement'] = 'zigbee'
                data['tags'] = {}
                data['tags']['sensor'] = sensor
                data['fields'] = {}
                data['fields']['battery'] = message['battery']
             
                if sensor == "temp":
                        data['fields']['humidity'] = message['humidity']
                        data['fields']['temperature'] = message['temperature']
                elif sensor == "smoke1" or sensor == "smoke2":
                        data['fields']['smoke'] = message['smoke']                
                try:
                        post_influx(json.dumps(data))
                        write_last_log(sensor)
                except:
                        pass


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.connect(config['DEFAULT']['mqtt_server'], config['DEFAULT']['mqtt_port'], 60)
mqttc.subscribe("zigbee2mqtt/#", 0)

mqttc.loop_forever()
