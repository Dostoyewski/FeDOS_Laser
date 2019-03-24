#!/usr/bin/env python3

import paho.mqtt.client as mqtt

broker="sandbox.rightech.io"
clientID = "tot_test"
userd = {"login": "admin", "pw": "admin"}

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("gcode")

def on_message(client, userdata, msg):
  print(msg.payload.decode())
    
client = mqtt.Client(clientID, True, None, mqtt.MQTTv31)
client.username_pw_set(username=userd["login"],password=userd["pw"])
client.connect(broker)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()