import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
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

# Работа с сообщениями
client = mqtt.Client(client_id=clientID)            
client.username_pw_set(username=userd["login"],password=userd["pw"])
client.on_connect=on_connect 
client.on_disconnect=on_disconnect
client.on_publish = on_publish
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker) 
# Основной цикл

vk_session = vk_api.VkApi(token='b3c988bf6f486085103feb412f78eb611af7597c9652183edd98f0410e4e04d7e7e42d4c74c745a775a80')
vk = vk_session.get_api()

longpoll = VkLongPoll(vk_session)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        print('id{}: "{}"'.format(event.user_id, event.text), end=' ')
        if (event.text=="reset"):
            client.publish('gcode', 'G0 X0 Y0')
            vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Система возвращена в начальное положение"
                    )
        else:
            if (event.text == "help"):
                vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Для помощи по командам GCode наберите 'help gcode', для помощи по общим командам наберите 'help general'"
                        )
            else:
                (com, ctx) = event.text.split(maxsplit=1)
                if(com == "help"):
                    if(ctx == "general"):
                        vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Список поддерживаемых команд:\n 1) reset - сброс в исходное состояние\n"
                                "2) print <URL> - вывод на печать загруженной картинки\n"
                                "3) publish <topic> <message> - ввод команд gcode напрямую (топик gcode для управления станцией)\n"
                                "4) draw <fig> <size> - вывод на печать заранее звгруженных фигур. Список фигур: square, star, circle."
                        )
                    if(ctx == "gcode"):
                        vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Список основных команд gcode для 'Цифровой Лазерной фабрики - альфа'\n:
                        "1) G0 X<float> Y<float> - перемещение манипулятора в точку X, Y в глобальных координатах\n"
                        "2) M106 - включение лазера\n"
                        "3) M107 - отключение лазера\n"
                        )
                if (com=="print"):
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Печать картинки..."
                        )
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
                        vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Рисуем квадрат..."
                        )
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
                        vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Квадрат нарисован."
                        )
                    if (fig=="circle"):
                        vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Рисуем круг..."
                        )
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
                        vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Круг нарисован."
                        )
                    if (fig=="star"):
                        vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Рисуем звезду..."
                        )
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
                        vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Звезда нарисована."
                        )
                
            
client.loop_stop()
client.disconnect() 