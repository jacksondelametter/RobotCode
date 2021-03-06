import RPi.GPIO as GPIO
import time
import socket
import struct
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

TIME_LIMIT = 1
COMMAND_ARM = 200
COMMAND_REST_ARM = 0
COMMAND_INITIATE_ARM = 1

INPUT_FORMAT = 'i i'

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


def connectToNetworkHub():
    global networkHubSocket
    global previousTime
    networkHubSocket = socket.socket()
    hostname = socket.gethostname()
    port = 4001
    #networkHubSocket.connect((hostname, port))
    #print("Connected to network hub")
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
    runMotor(MOTOR_0, 0)
    runMotor(MOTOR_1, 0)
    runMotor(MOTOR_2, 0)

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
while(1):
    try:
        #timer = Timer(3, stopCommand)
        #timer.start()
        print("Waiting...")
        unpackedCommand = networkHubSocket.recv(struct.calcsize(INPUT_FORMAT))
        #timer.cancel()
        command = struct.unpack(INPUT_FORMAT, unpackedCommand)
        print(command)
        leftPower = command[0]
        rightPower = command[1]
        runMotors(leftPower, rightPower)
    except KeyboardInterrupt:
        stopMotors()
        #closeConnections()
        break
    except:
        print('Program Error')
        #closeConnections()
        connectToNetworkHub()
        



