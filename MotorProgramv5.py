import RPi.GPIO as GPIO
import time
import socket
import struct
import select
import sys
from threading import Timer

ENA = 4
ENB = 16
IN1 = 17
IN2 = 18
IN3 = 12
IN4 = 13
motot1 = None
motor2 = None
networkHubSocket = None
previousTime = None
automationHubSocket = None

TIME_LIMIT = 1
COMMAND_ARM = 200
COMMAND_REST_ARM = 0
COMMAND_INITIATE_ARM = 1

frontSensorClear = True
backSensorClear = True
rightSensorClear = True
leftSensorClear = True

INPUT_FORMAT = 'i i'
AUTOMATION_FORMAT = '? ? ? ?'

def setup():
    global motor1
    global motor2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
    motor1 = GPIO.PWM(ENA, 2000)
    motor2 = GPIO.PWM(ENB, 2000)
    motor1.start(0)
    motor2.start(0)

def moveForward():
    global motor1
    global motor2
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    motor1.start(80)
    motor2.start(80)

def moveBackward():
    global motor1
    global motor2
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    motor1.start(80)
    motor2.start(80)
    

def runMotors(leftPower, rightPower):
    global motor1
    global motor2
    global frontSensorClear
    global backSensorClear
    global rightSensorClear
    global leftSensorClear
    absRightPower = abs(rightPower)
    absLeftPower = abs(leftPower)
    if (rightPower > 0 and rightPower == leftPower and not frontSensorClear):
        # Motors trying to go front and sensor not clear
        print('Front sensors not clear')
        leftPower = 0
        rightPower = 0
    if (rightPower < 0 and rightPower == leftPower and not backSensorClear):
        # Motors trying to go back and sensor not clear
        print('Back sensors not clear')
        leftPower = 0
        rightPower = 0
    elif (absRightPower < absLeftPower and not rightSensorClear):
        # Motors trying to turn right and right sensor not clear
        print('Right sensor not clear')
        leftPower = 0
        rightPower = 0
    elif (absRightPower > absLeftPower and not leftSensorClear):
        # Motors trying to turn left and left sensor not clear
        print('Left sensor not clear')
        leftPower = 0
        rightPower = 0
    elif (rightPower < leftPower and absRightPower == absLeftPower and not rightSensorClear):
        # Motors are spinning right and right sensor not clear
        print('Right sensor not clear')
        leftPower = 0
        rightPower = 0
    elif (rightPower > leftPower and absRightPower == absLeftPower and not leftSensorClear):
        # Motors are spinning left and left sensor not clear
        print('left sensor not clear')
        leftPower = 0
        rightPower = 0
        
    if (leftPower >= 0):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        motor1.start(abs(leftPower))
    elif (leftPower < 0):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        motor1.start(abs(leftPower))

    if (rightPower >= 0):
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        motor2.start(abs(rightPower))
    elif (rightPower < 0):
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        motor2.start(abs(rightPower))

def connectToAutomationHub():
    global automationHubSocket
    automationHubSocket = socket.socket()
    automationHubSocket.setblocking(0)
    hostname = socket.gethostname()
    port = 4002
    while(1):
        time.sleep(0.5)
        print("Connecting to automation hub")
        try:
            automationHubSocket.connect((hostname, port))
            print('Connected to automation hub')
            break
        except socket.error as e:
            print('Cant connect to automation hub')
            automationHubSocket.close
        except KeyboardInterrupt:
            print("Program Ended")
            automationHubSocket.close
            sys.exit()

def connectToNetworkHub():
    global networkHubSocket
    networkHubSocket = socket.socket()
    networkHubSocket.setblocking(0)
    hostname = socket.gethostname()
    port = 4001
    while(1):
        time.sleep(0.5)
        print("Connecting to network hub")
        try:
            networkHubSocket.connect((hostname, port))
            print('Connected to network hub')
            break
        except socket.error as e:
            print('Cant connect to network hub')
            networkHubSocket.close
        except KeyboardInterrupt:
            print("Program Ended")
            networkHubSocket.close
            sys.exit()

def chooseMotor():
    global activeMotor
    motorNum = input('Choose Motor')
    if(motorNum == MOTOR_0):
        activeMotor = motorNum
    elif(motorNum == MOTOR_1):
        activeMotor = motorNum
    elif(motorNum == MOTOR_2):
        activeMotor = motorNum
    else:
        activeMotor = MOTOR_0

def stopMotors():
    runMotors(0, 0)

def closeConnections():
    global networkHubSocket
    shutdownSocket(networkHubSocket)

def stopCommand():
    closeConnections()
    connectToNetworkHub()

def shutdownSocket(socket):
    try:
        socket.shutdown(socket.SHUT_RDWR)
        socket.close
    except:
        print("Socket already closed")

setup()
connectToNetworkHub()
connectToAutomationHub()
while(1):
    try:
        print("Waiting...")
        readable, writable, exceptional = select.select([networkHubSocket, automationHubSocket], [], [])
        for socket in readable:
            if socket is networkHubSocket:    
                unpackedCommand = socket.recv(struct.calcsize(INPUT_FORMAT))
                command = struct.unpack(INPUT_FORMAT, unpackedCommand)
                print(command)
                leftPower = command[0]
                rightPower = command[1]
                runMotors(leftPower, rightPower)
            elif socket is automationHubSocket:
                packedCommand = socket.recv(struct.calcsize(AUTOMATION_FORMAT))
                command = struct.unpack(AUTOMATION_FORMAT, packedCommand)
                print(command)
                frontSensorClear = command[0]
                backSensorClear = command[1]
                rightSensorClear = command[2]
                leftSensorClear = command[3]
    except KeyboardInterrupt:
        stopMotors()
        break
    except:
        print('Program Error')
        stopMotors()
        break
        



