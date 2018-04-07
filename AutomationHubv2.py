import RPi.GPIO as GPIO
import time
import socket
import struct
GPIO.setmode(GPIO.BCM)

#global variables

LEFT = 0
RIGHT = 1
FRONT = (18, 23)
BACK = 3

FRONT_SEN_THRESH = 10
BACK_SEN_THRESH = 10
LEFT_SEN_THRESH = 10
RIGHT_SEN_THRESH = 10

motorServerSocket = None
motorSocket = None

##functions left to implement that are used in code already:
##  turnRobotRight(Degree amount)
##  turnRobotLeft(Degree amount)
##  driveRobotForward(distance amount)
##  driveForward(speed)

def setupSensors():
    GPIO.setup(FRONT[0],GPIO.OUT)
    GPIO.setup(FRONT[1],GPIO.IN)
    GPIO.output(FRONT[0], False)
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
    print distance, "cm"
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
    frontSensor = sensorRead(FRONT)
    if frontSensor > FRONT_SEN_THRESH:
        front = True
    else:
        front = False
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
    data = struct.pack('? ? ? ?', front, back, right, left)
    motorSocket.send(data)
    time.sleep(0.5)
        
