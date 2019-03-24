import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
import urllib.request
import paho.mqtt.client as mqtt
import time
from PIL import Image
import numpy as np
import math



def procImage(path):
    im = Image.open(path)
    #bg = Image.new("RGB", im.size, (255,255,255))
    #bg.paste(im,im)
    bg = im.resize((110, 110))
    bg = bg.convert('1')
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
client = mqtt.Client(client_id=clientID)            
client.username_pw_set(username=userd["login"],password=userd["pw"])
client.on_connect=on_connect 
client.on_disconnect=on_disconnect
client.on_publish = on_publish
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker) 

def main():
    session = requests.Session()
    # Авторизация пользователя:
    """
    login, password = 'python@vk.com', 'mypassword'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    """

    # Авторизация группы (для групп рекомендуется использовать VkBotLongPoll):
    # при передаче token вызывать vk_session.auth не нужно

    vk_session = vk_api.VkApi(token='b3c988bf6f486085103feb412f78eb611af7597c9652183edd98f0410e4e04d7e7e42d4c74c745a775a80')
    for i in range(0, len(vid)):
        vid[i] = 0
    vk = vk_session.get_api()

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)
    isFound = False
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print('id{}: "{}"'.format(event.user_id, event.text), end=' ')
            print(isFound)
            for i in range(0, len(vid)):
                if(int(event.user_id - vid[i]) == 0):
                    print("Found")
                    isFound = True
                    text = "Здравствуйте, " + names[i]
                    vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=text
                    )
                    break
                    
            
            if (event.text=="reset"):
                client.publish('gcode', 'G0 X0 Y0')
            else:  
                (com, ctx) = event.text.split(maxsplit=1)
                if (com=="print"):
                    urllib.request.urlretrieve(ctx, "image.jpg")
                    
                if (com=="publish"):
                    (topic, payment) = ctx.split(maxsplit=1)
                    client.publish(topic, payment)
                if (com=="draw"):
                    (fig, size) = ctx.split(maxsplit=1)
                    if (fig=="square"):
                        client.publish("gcode", "G0 X0 Y0")
                        time.sleep(2)
                        client.publish("gcode", "G0 X"+size+" Y0")
                        time.sleep(2)
                        client.publish("gcode", "G0 X"+size+" Y"+size)
                        time.sleep(2)
                        client.publish("gcode", "G0 X0 Y"+size)
                        time.sleep(2)
                        client.publish("gcode", "G0 X0 Y0")
                        time.sleep(2)
                    if (fig=="circle"):
                        client.publish("gcode", "G0 X50 Y50")
                        time.sleep(5)
                        for t in range(40):
                            client.publish("gcode", "G0 X"+str(30+round(int(size)*math.cos(2*math.pi*t/39)))+" Y"+str(50+round(int(size)*math.sin(2*math.pi*t/39))))
                            time.sleep(1)
                        client.publish("gcode", "G0 X0 Y0")
                    if (fig=="star"):
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
                        time.sleep(2)
                        client.publish("gcode", "G0 X0 Y0")
                
client.loop_stop()

