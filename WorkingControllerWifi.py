import socket
import pygame
from time import sleep
import sys
import struct
import threading

##initial data for analog and variables for threading
analogData = b'm\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
stopThread = False
c = None

##thread that sends data for analog and if the data doesn't send, reconnects
def sendData():
    global analogData
    global c

    if stopThread == False:
        threading.Timer(0.1, sendData).start()
        try:
            c.send(analogData)
        except:
            print("failed")
            c.close()
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.connect((hostname,port))
            print("Connected")
    else:
        print("closing")

##Modifies the value from the analog based on region of the stick into
##power levels for motors. Then packs it into the sending packet
def writeFunction(X,Y):
    global analogData
    
    left = 0
    right = 0
    
    if Y > 0.40:
        Y = -((((Y-0.40)/0.60)*35)+65)
    elif Y < -0.40:
        Y = -((((Y+0.40)/0.60)*35)-65)
    elif Y > 0.05 and Y < 0.40:
        Y = -((((Y-0.05)/0.35)*5)+60)
    elif Y < -0.05 and Y > -0.40:
        Y = -((((Y+0.05)/0.35)*5)-60)
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
    analogData = struct.pack('cii?', b'm', left, right, sensorStatus)

##Prevents the analog stick from returning values above 1 or below -1. Also
##makes a dead zone in the center of the analog stick so the stick will always
##read zero at the center.
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

##global variables
left = 0
right = 0
servoList = [0,4,5,6,2]
servoCount = 0
sensorStatus = True

##pygame initialize and create controller
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

##competition IP and port
#hostname = '139.78.85.131'
#port = 11000
hostname = '192.168.2.2'
port = 1234

##initializes socket
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((hostname,port))
print("Connected")

##starts thread for sending analog data
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
                #options button
                if event.button == 9:
                    #sets sensors on or off for sending with data
                    if sensorStatus:
                        sensorStatus = False
                        print("Sensors are OFF")
                    else:
                        sensorStatus = True
                        print("Sensors are ON")
                #this is R1
                if event.button == 5:
                    data = struct.pack('cii?',b's', 1, 0, sensorStatus)
                    c.send(data)
                #this is L1
                if event.button == 4:
                    data = struct.pack('cii?',b's', 0, 0, sensorStatus)
                    c.send(data)
                #this is R2
                if event.button == 7:
                    data = struct.pack('cii?',b's', 2, 0, sensorStatus)
                    c.send(data)
                #this is L2
                if event.button == 6:
                    data = struct.pack('cii?',b's', 3, 0, sensorStatus)
                    c.send(data)
                #this is square
                if event.button == 0:
                    if servoCount != 4:
                        servoCount += 1
                    else:
                        servoCount = 0
                    #prints directions for current servo
                    servo = servoList[servoCount]
                    print(servoCount)
                    if servo == 0:
                        print("current servo = Base")
                        print("Up/Right = Back, Down/Left = Forward")
                    elif servo == 4:
                        print("current servo = Lower")
                        print("Up/Right = Up, Down/Left = Down")
                    elif servo == 5:
                        print("current servo = Upper")
                        print("Up/Right = Down, Down/Left = Up")
                    elif servo == 6:
                        print("current servo = Rotate")
                        print("Up/Right = Clock, Down/Left = CounterClock")
                    elif servo == 2:
                        print("current servo = Claw")
                        print("Up/Right = Close, Down/Left = Open")
                #this is share
                if event.button == 8:
                    stopThread = True
                    print("Closing")
                    c.close
                    print("Good Bye")
                    sys.exit(1)
                    break
            #checks directional pad on controller
            elif event.type == pygame.JOYHATMOTION:
                if event.value[0] == -1:
                    data = struct.pack('cii?',b'c', servo, -30, sensorStatus)
                    c.send(data)
                if event.value[0] == 1:
                    data = struct.pack('cii?',b'c', servo, 30, sensorStatus)
                    c.send(data)
                if event.value[1] == -1:
                    data = struct.pack('cii?',b'c', servo, -10, sensorStatus)
                    c.send(data)
                if event.value[1] == 1:
                    data = struct.pack('cii?',b'c', servo, 10, sensorStatus)
                    c.send(data)
except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()
