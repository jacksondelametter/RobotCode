import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#global variables
robotWidth = 10
heading = 0
center = 0
mode = 0

MANUAL = 0
AUTOMATIC = 1
SPRINT = 2

LEFT = 0
RIGHT = 1
FRONT = 2
BACK = 3

##functions left to implement that are used in code already:
##  turnRobotRight(Degree amount)
##  turnRobotLeft(Degree amount)
##  driveRobotForward(distance amount)
##  driveForward(speed)

def sensorRead(senNum):
    #set pin of sensor here
    TRIG = 23
    ECHO = 24

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(.00002)

    GPIO.output(TRIG, True)
    time.sleep(.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
            pulse_start = time.time()
    while GPIO.input(ECHO)==1:
            pulse_end = time.time()
    pulse = pulse_end - pulse_start
    distance = pulse * 17150
    return distance
    print round(distance, 1), "cm"

def beginSprint():
    #put sprint code here
    print("SPRINT")

def beginDrive():
    driveForward(cruiseSpeed)
    while(driveClear):
        #fill this in
        print("not finished")

def beginCorrection():
    front = False
    right = False
    left = False
    back = False
    
    while mode == MANUAL:
        if sensorRead(FRONT) < 2.55:
            front = True
        else:
            front = False
        if sensorRead(RIGHT) < 10.17:
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
            back = False
        data = struct.pack('? ? ? ?', front, right, left, back)
        c.send(data)

def centerTrack():
    while(sensorRead(LEFT) < (sensorCenter+LIMIT) and sensorRead(LEFT) > (sensorCenter-LIMIT)):
        #find center limit of error to fill for LIMIT
        if sensorRead(LEFT) > (sensorCenter+LIMIT):
            driveAmount = sensorRead(LEFT) - sensorCenter
            turnRobotLeft(90)
            #will need IMU to track this
            driveRobotForward(driveAmount)
            turnRobotRight(90)
        else:
            driveAmount = sensorCenter - sensorRead(LEFT)
            turnRobotRight(90)
            driveRobotForward(driveAmount)
            turnRobotLeft(90)


def startUp():
    #global variable
    global center
    global heading
    global sensorCenter
          
    #function to turn robot by X degrees
    turnRobotLeft(90)
    curRead = -2
    prevRead = -1
    while(curRead <= prevRead):
        turnRobotRight(1)
        prevRead = curRead
        #read in left sensor
        curRead = sensorRead(LEFT)
    turnRobotLeft(1)
    #here the current postion needs updated for directional tracking
    heading = 0
    center = (sensorRead(LEFT) + sensorRead(RIGHT) + robotWidth)/2
    sensorCenter = center - (robotWidth/2)
    centerTrack()


#Main code

#client
#needs set up for local
hostname = '192.168.2.4'
port = 1234
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((hostname,port))
print("Connected")

startUp()
while True:
    if mode == MANUAL:
        beginCorrection()
    elif mode == AUTOMATIC:
        startUp()
        beginDrive()
    elif mode == SPRINT:
        beginSprint()
    elif mode == DISABLE:
        
