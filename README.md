# zigbee-mqtt-parser
Simple parser to collect MQTT messages and to relay those to Influx DB

#### How it works ####

#### Prerequisites ####

#### Sample cron job ####

#### Sample config file (default.config) ####
```python
[DEFAULT]
#Influx DB params
influx_host = myweb.com
influx_port = 8086
influx_user = myuser
influx_pass = mypass
influx_db = mydb

#MQTT parser
mqtt_server = localhost
mqtt_port = 1883
```
