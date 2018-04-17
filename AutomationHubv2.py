import RPi.GPIO as GPIO
import time
import socket
import struct
GPIO.setmode(GPIO.BCM)

#global variables

LEFT = (12, 13)
RIGHT = (5, 6)
FRONT = (6, 9)
BACK = 3

FRONT_SEN_THRESH = 10
BACK_SEN_THRESH = 10
LEFT_SEN_THRESH = 20
RIGHT_SEN_THRESH = 20

motorServerSocket = None
motorSocket = None

##functions left to implement that are used in code already:
##  turnRobotRight(Degree amount)
##  turnRobotLeft(Degree amount)
##  driveRobotForward(distance amount)
##  driveForward(speed)

def setupSensors():
    GPIO.setup(RIGHT[0],GPIO.OUT)
    GPIO.setup(RIGHT[1],GPIO.IN)
    GPIO.output(RIGHT[0], False)
    GPIO.setup(LEFT[0],GPIO.OUT)
    GPIO.setup(LEFT[1],GPIO.IN)
    GPIO.output(LEFT[0], False)
    print('Settings up sensors')
    time.sleep(2)

def sensorRead(senNum):
    global LEFT
    global RIGHT
    global FRONT
    global BACK

    GPIO.output(senNum[0], True)
    time.sleep(.00001)
    GPIO.output(senNum[0], False)
    #print('About to read sensor')

    while GPIO.input(senNum[1])==0:
        #print('Echo still 0')
        pulse_start = time.time()
    while GPIO.input(senNum[1])==1:
        #print('Echo still 1')
        pulse_end = time.time()
    pulse = pulse_end - pulse_start
    distance = pulse * 17150
    distance = round(distance, 2)
    return distance

def setupMotorProgramConnection():
    global motorServerSocket
    global motorSocket
    motorServerSocket = socket.socket()
    hostname = socket.gethostname()
    port = 4002
    while(1):
        print('Waiting for motor program')
        try:
            motorServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            motorServerSocket.bind((hostname, port))
            motorServerSocket.listen(100)
            print("Created motor program connection")
            break
        except:
            print('Couldnt make motor program connection')
    motorSocket, addr = motorServerSocket.accept()
    print('Connected to motor program')


#Main code

#client
#needs set up for local
setupMotorProgramConnection()
setupSensors()
#startUp()
while (1):
    front = True
    right = True
    left = True
    back = True
    rightSensor = sensorRead(RIGHT)
    leftSensor = sensorRead(LEFT)
    if rightSensor < RIGHT_SEN_THRESH:
        print('Right to low')
        right = False
    else:
        right = True

    if leftSensor < LEFT_SEN_THRESH:
        print('left to low')
        left = False
    else:
        left = True
    '''if sensorRead(RIGHT) < 10.17:
        right = True
    else:
        right = False
    if sensorRead(LEFT) < 10.17:
        left = True
    else:
        left = False
    if sensorRead(BACK) < 2.55:
        back = True
    else:
        back = False'''
    print('Right Sensor: ' + str(rightSensor) + '\n' + 'Left Sensor: ' + str(leftSensor))
    data = struct.pack('? ? ? ?', front, back, right, left)
    motorSocket.send(data)
    time.sleep(0.5)
        
