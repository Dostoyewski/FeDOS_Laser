import paho.mqtt.client as mqtt
import time
from PIL import Image
import numpy as np

def procImage(path):
    im = Image.open(path)
    #bg = Image.new("RGB", im.size, (255,255,255))
    #bg.paste(im,im)
    bg = im.resize((110, 110))
    bg = bg.convert('1')
    pix = np.array(bg)
    return pix


    
broker="sandbox.rightech.io"
clientID = "tot_test"
userd = {"login": "admin", "pw": "admin"}

def on_connect(client, userdata, flags, rc):
    client.publish("bot_online", 1)
    if rc==0:
        print("Bot connected OK")
    else:
        print("Bad connection Returned code=",rc)
        
def on_disconnect(client, userdata, rc):
    client.publish("bot_online", 0)
    print("Disconnected")

def on_publish(client, userdata, rc):
    print("Data published")
    
client = mqtt.Client(client_id=clientID)            
client.username_pw_set(username=userd["login"],password=userd["pw"])
client.on_connect=on_connect 
client.on_disconnect=on_disconnect
client.on_publish = on_publish
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker)     
while True: 
    print("Waiting for command...")
    text = input()
    if (text=="stop"):
        client.publish("bot_online", 0)
        break
    (com, topic, content) = text.split(maxsplit=2)
    #print(com, topic, content)
    if (com=="p"):
        client.publish(topic, content)
    if (com=="print"):
        px = procImage(topic)
    time.sleep(1)
client.loop_stop()
client.disconnect() 

input()