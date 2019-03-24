import paho.mqtt.client as mqtt
import time
import serial
ser = serial.Serial("COM3", 115200)

broker="sandbox.rightech.io"
clientID = "tot_test2"
userd = {"login": "admin", "pw": "admin"}

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True 
        print("Raspberry connected OK")
        #client.publish("rb_online", 1, qos=2)
        print("subscribing ")
        client.subscribe("gcode")
    else:
        print("Bad connection Returned code=",rc)
        
        
def on_disconnect(client, userdata, rc):
    #client.publish("rb_online", 0, qos=2)
    print("Disconnected")

def on_publish(client, userdata, rc):
    print("Data published")
    
def on_message(client, userdata, message):
    #time.sleep(1)
    msg=str(message.payload.decode("utf-8"))
    print("Received message =",msg)
    if ser.isOpen():
      
        try:
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output
            
            #time.sleep(1)
      
            
            ser.write((msg+'\n').encode('utf-8'))
            #time.sleep(11)
            print("write data:",msg)
                    
      
        except Exception as e1:
            print ("error communicating...: " + str(e1))
            
    else:
        print( "cannot open serial port ")
        
    
sub = mqtt.Client(client_id=clientID)
sub.username_pw_set(username=userd["login"],password=userd["pw"])
sub.on_connect=on_connect 
sub.on_disconnect=on_disconnect
sub.on_publish = on_publish
sub.on_message = on_message
sub.loop_start()
print("Connecting to broker ",broker)
sub.connect(broker)    
while True:
    print("Waiting for commands...")
    text = input()
    if (text=="stop"):
        break
sub.loop_stop()
sub.disconnect() 
ser.close()
input()