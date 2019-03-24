#!/usr/bin/python
  
import serial
import time
#initialization and open the port
#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call
ser = serial.Serial("COM3", 115200)
  
if ser.isOpen():
  
    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output
                 #and discard all that is in buffer
  
        #write data
  
        time.sleep(1)  #give the serial port sometime to receive the data
  
        numOfLines = 0
  
        while True:
            response = ser.readline()
            print("read data: " + response.decode('utf-8'))
  
            numOfLines = numOfLines + 1
  
            if (numOfLines == 37):
                ser.write(b"echo: G0 X100 Y100")
                print("write data: G0 X100 Y100")
                
  
        ser.close()
    except Exception as e1:
        print ("error communicating...: " + str(e1))
        
else:
    print( "cannot open serial port ")
input()