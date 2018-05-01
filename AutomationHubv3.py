import RPi.GPIO as GPIO
import time
import socket
import struct
GPIO.setmode(GPIO.BCM)

#global variables

LEFT = (12, 13)
RIGHT = (5, 6)
FRONT = (16, 19)

FRONT_SEN_THRESH = 10
LEFT_SEN_THRESH = 20
RIGHT_SEN_THRESH = 20

ZONE1_THRESH = 14
ZONE2_THRESH = 8
ZONE3_THRESH = 14
ZONE4_THRESH = 8
ZONE5_THRESH = 15

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
    GPIO.setup(FRONT[0],GPIO.OUT)
    GPIO.setup(FRONT[1],GPIO.IN)
    GPIO.output(FRONT[0], False)
    print('Automation Hub: Settings up sensors')
    time.sleep(2)

def sensorRead(senNum):
    global LEFT
    global RIGHT
    global FRONT

    distance = 0
    pulse_start = time.time()
    pulse_end = time.time()
    GPIO.output(senNum[0], True)
    time.sleep(.00001)
    GPIO.output(senNum[0], False)
    #print('About to read sensor')

    while GPIO.input(senNum[1])==0:
        pulse_start = time.time()
        if pulse_start - pulse_end > .02:
            distance = 100
            break
    while GPIO.input(senNum[1])==1:
        pulse_end = time.time()
        if pulse_start - pulse_end > .02:
            distance = 100
            break

    pulse_duration = pulse_end - pulse_start
    if distance != 100:
        distance = pulse_duration * 17150

    distance = round(distance, 2)

    return distance

def setupMotorProgramConnection():
    global motorServerSocket
    global motorSocket
    motorServerSocket = socket.socket()
    hostname = socket.gethostname()
    port = 4002
    while(1):
        print('AutomaWaiting for motor program')
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
    frontSensor = sensorRead(FRONT)
    zone = 0
    if (frontSensor <= ZONE5_THRESH):
        print('front to low')
        zone = 5
    elif (rightSensor <= ZONE4_THRESH):
        print('right way to low')
        zone = 4
    elif (rightSensor <= ZONE3_THRESH):
        print('right to low')
        zone = 3
    elif (leftSensor <= ZONE2_THRESH):
        print('left way to low')
        zone = 2
    elif (leftSensor <= ZONE1_THRESH):
        print('left to low')
        zone = 1
    else:
        print('sensors clear')
        zone = 0
    print('Right Sensor: ' + str(rightSensor) + '\n' + 'Left Sensor: ' + str(leftSensor) + '\n' + 'Front Sensor: ' + str(frontSensor))
    data = struct.pack('i', zone)
    #print('Right Sensor: ' + str(rightSensor) + '\n' + 'Left Sensor: ' + str(leftSensor) + '\n')
    motorSocket.send(data)
    #time.sleep(0.1)
        
