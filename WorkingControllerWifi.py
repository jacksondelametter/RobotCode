import socket
import pygame
from time import sleep
import sys
import struct
import threading

analogData = b'm\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def sendData():
    global analogData
    
    threading.Timer(0.1, sendData).start()
    #print(analogData)
    c.send(analogData)

def writeFunction(X,Y):
    global analogData
    
    left = 0
    right = 0
    if Y > 0:
        Y = -(((((Y*100)-5)/95)*70)+30)
    elif Y < 0:
        Y = -(((((Y*100)+5)/95)*70)-30)
    else:
        Y = 0
    if X>0.995:
        left = Y
        right = -Y
    elif X<-0.995:
        left = -Y
        right = Y
    elif X > 0:
        right = Y*(1-(X))
        left = Y
    elif X < 0:
        left = Y*(1+(X))
        right = Y
    else:
        left = Y
        right = Y
    left = int(left)
    right = int(right)
    analogData = struct.pack('c i i', b'm', left, right)
    #print("%i , %i" % left, right)
    #print("%s is analog Data" % analogData)
    #print(data)
    #c.send(data)

def joystickNumProc(X,Y):
    if X > -0.05 and X < 0.05:
        X = 0
    if Y > -0.05 and Y < 0.05:
        Y = 0
    #correct error over/under 1/-1
    if X > 1:
        X = 1
    elif X < -1:
        X = -1
    
    if Y > 1:
        Y = 1
    elif Y < -1:
        Y = -1

    writeFunction(X,Y)

#global variables?
left = 0
right = 0
servoList = [0,4,5,6,7]

#pygame initialize and create controller
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

#create server
##s = socket.socket()
##hostname = socket.gethostname()
##port = 5001
##s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
##s.bind((hostname, port))
##s.listen(5)

hostname = '192.168.2.2'
port = 1234
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((hostname,port))
print("Connected")

##c, addr = s.accept()
##print("Got connection")
sendData()
try:
    while True:
        events = pygame.event.get()
        for event in events:
            #check joysticks
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 1:
                    joystickNumProc(j.get_axis(2), event.value)
                elif event.axis == 2:
                    joystickNumProc(event.value, j.get_axis(1))
            #check buttons
            elif event.type == pygame.JOYBUTTONDOWN:
                #this is R1
                if event.button == 5:
##                    left = 1
##                    right =  0
                    data = struct.pack('c i i',b's', 1, 0)
                    c.send(data)
                #this is L1
                if event.button == 4:
##                    left = 0
##                    right =  0
                    data = struct.pack('c i i',b's', 0, 0)
                    #print("%s is data" % data)
                    c.send(data)
                #this is R2
                if event.button == 7:
##                    left = 2
##                    right =  0
                    data = struct.pack('c i i',b's', 2, 0)
                    c.send(data)
                #this is L2
                if event.button == 6:
##                    left = 3
##                    right =  0
                    data = struct.pack('c i i',b's', 3, 0)
                    c.send(data)
                #this is square
                if event.button == 0:
                    if servoCount != 4:
                        print("add")
                        servoCount += 1
                    else:
                        print("reset")
                        servoCount = 0
                    servo = servoList[servoCount]
                    print(servoCount)
                    print("current servo = %i" % servo)
                #this is circle
                if event.button == 2:
##                    left = 4
##                    right =  0
                    data = struct.pack('c i i',b's', 4, 0)
                    c.send(data)
                if event.button == 3:
                    print("Closing")
                    #s.close
                    c.close
                    print("Good Bye")
                    sys.exit(1)
                    break
            #checks directional pad on controller
            elif event.type == pygame.JOYHATMOTION:
##                if event.value[0] == -1:
##                    data = struct.pack('c i i',b'c', servo, -30)
##                    c.send(data)
##                if event.value[0] == 1:
##                    data = struct.pack('c i i',b'c', servo, 30)
##                    c.send(data)
##                if event.value[1] == -1:
##                    data = struct.pack('c i i',b'c', servo, -10)
##                    c.send(data)
##                if event.value[1] == 1:
##                    data = struct.pack('c i i',b'c', servo, 10)
##                    c.send(data)
                print("Broken")
except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()
