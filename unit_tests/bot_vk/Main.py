import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import urllib.request
import paho.mqtt.client as mqtt
import time
from PIL import Image
import numpy as np
import math
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message})


def procImage(path):
    im = Image.open(path)
    #bg = Image.new("RGB", im.size, (255,255,255))
    #bg.paste(im,im)
    bg = im.resize((20, 20))
    bg = bg.convert('1')
    bg.save('out.jpg')
    pix = np.array(bg)
    return pix

def on_connect(client, userdata, flags, rc):
    client.publish("bot_online", 1)
    if rc==0:
        print("Bot connected OK")
    else:
        print("Bad connection Returned code=",rc)
        
def on_disconnect(client, userdata, rc):
    client.publish("bot_online", 0)
    print("Disconnected", rc)

def on_publish(client, userdata, rc):
    print("Data published")

broker="sandbox.rightech.io"
clientID = "tot_test"
userd = {"login": "admin", "pw": "admin"}
# API-ключ созданный ранее
token = "b3c988bf6f486085103feb412f78eb611af7597c9652183edd98f0410e4e04d7e7e42d4c74c745a775a80"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)
client = mqtt.Client(client_id=clientID)            
client.username_pw_set(username=userd["login"],password=userd["pw"])
client.on_connect=on_connect 
client.on_disconnect=on_disconnect
client.on_publish = on_publish
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker) 
# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        if (event.text=="reset"):
            client.publish('gcode', 'G0 X0 Y0')
        else:  
            (com, ctx) = event.text.split(maxsplit=1)
            if (com=="print"):
                urllib.request.urlretrieve(ctx, "image.jpg")
                px = procImage("image.jpg")
                for i in range(20):
                    for j in range(20):
                        client.publish("gcode", "G0 X"+str(i)+" Y"+str(j))
                        if (px[i][j]):
                            client.publish("gcode", "M106")
                        time.sleep(0.5)
                        client.publish("gcode", "M107")
                        
                
            if (com=="publish"):
                (topic, payment) = ctx.split(maxsplit=1)
                client.publish(topic, payment)
            if (com=="draw"):
                (fig, size) = ctx.split(maxsplit=1)
                if (fig=="square"):
                    client.publish("gcode", "M106")
                    time.sleep(0.5)
                    client.publish("gcode", "G0 X0 Y0")
                    time.sleep(2)
                    client.publish("gcode", "G0 X"+size+" Y0")
                    time.sleep(2)
                    client.publish("gcode", "G0 X"+size+" Y"+size)
                    time.sleep(2)
                    client.publish("gcode", "G0 X0 Y"+size)
                    time.sleep(2)
                    client.publish("gcode", "G0 X0 Y0")
                    time.sleep(0.5)
                    client.publish("gcode", "M107")
                if (fig=="circle"):    
                    client.publish("gcode", "G0 X50 Y50")
                    time.sleep(5)
                    client.publish("gcode", "M106")
                    time.sleep(0.5)
                    for t in range(40):
                        client.publish("gcode", "G0 X"+str(30+round(int(size)*math.cos(2*math.pi*t/39)))+" Y"+str(50+round(int(size)*math.sin(2*math.pi*t/39))))
                        time.sleep(1)
                    time.sleep(0.5)
                    client.publish("gcode", "M107")
                    client.publish("gcode", "G0 X0 Y0")
                if (fig=="star"):
                    client.publish("gcode", "M106")
                    client.publish("gcode", "G0 X50 Y50")
                    time.sleep(2)
                    client.publish("gcode", "G0 X70 Y50")
                    time.sleep(2)
                    client.publish("gcode", "G0 X30 Y38")
                    time.sleep(2)
                    client.publish("gcode", "G0 X62 Y70")
                    time.sleep(2)
                    client.publish("gcode", "G0 X62 Y30")
                    time.sleep(2)
                    client.publish("gcode", "G0 X30 Y62")
                    time.sleep(2)
                    client.publish("gcode", "G0 X70 Y50")
                    time.sleep(0.5)
                    client.publish("gcode", "M107")
                    time.sleep(2)
                    client.publish("gcode", "G0 X0 Y0")
                    
            
            
client.loop_stop()
client.disconnect() 