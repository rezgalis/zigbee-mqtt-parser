
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, struct, json, configparser
import paho.mqtt.client as mqtt
from datetime import datetime
from influxdb import InfluxDBClient

basepath = '/home/pi/zigbee-mqtt-parser/'

config = configparser.ConfigParser()
config.read(basepath + 'default.config')

topics_to_influx = {"temp":datetime.now(), "smoke1": datetime.now(), "smoke2": datetime.now()} #in zigbee2mqtt/ channel

client = InfluxDBClient(config['DEFAULT']['influx_host'], config['DEFAULT']['influx_port'], config['DEFAULT']['influx_user'], config['DEFAULT']['influx_pass'], config['DEFAULT']['influx_db'])


def is_update_time(sensor):
	should_run_update = True	
	prev_time = topics_to_influx[sensor]
	diff = datetime.now() - prev_time
	if diff.seconds<30:
		should_run_update = False
	return should_run_update


def write_last_update(sensor):
	topics_to_influx[sensor] = datetime.now()


def post_influx(json_body):
	client.write_points([json_body])


def on_message(mqttc, obj, msg):
	sensor = str(msg.topic.split("/")[1])
	#print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	if topics_to_influx.has_key(sensor) and is_update_time(sensor):
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
			post_influx(data)
			write_last_update(sensor)
		except Exception, e:
			print e
			pass


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.connect(config['DEFAULT']['mqtt_server'], str(config['DEFAULT']['mqtt_port']), 60)
mqttc.subscribe("zigbee2mqtt/#", 0)

mqttc.loop_forever()
