import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        
        
def on_disconnect(client, userdata, rc):
    client.publish("online", 0)
    print("disconnected")
    logging.info("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True

def on_publish(client, userdata, rc):
    print("data published")
    
mqtt.Client.connected_flag=False#create flag in class
broker="sandbox.rightech.io"
client = mqtt.Client(client_id="tot_test")             #create new instance 
client.username_pw_set(username="admin",password="admin")
client.on_connect=on_connect  #bind call back function
client.on_disconnect=on_disconnect
client.on_publish = on_publish
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker)      #connect to broker
while not client.connected_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)
client.publish("online", 1)
client.publish("x", 50)
client.publish("y", 50)
print("in Main Loop")
client.loop_stop()    #Stop loop 
if (input()=="stop"):
    client.disconnect() # disconnect