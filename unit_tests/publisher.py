#!/usr/bin/env python3

import paho.mqtt.client as mqtt

broker="sandbox.rightech.io"
clientID = "tot_test"
userd = {"login": "admin", "pw": "admin"}

client = mqtt.Client(clientID, True, None, mqtt.MQTTv31)
client.username_pw_set(username=userd["login"],password=userd["pw"])
client.connect(broker)
client.publish("gcode", "Hello world!");
client.disconnect();
input()