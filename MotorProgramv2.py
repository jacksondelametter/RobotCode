import RPi.GPIO as GPIO
import time
import socket
import struct

ENA = 21
ENB = 16
IN1 = 2
IN2 = 15
IN3 = 23
IN4 = 25
motot1 = None
motor2 = None

FORWARD = "1"
BACKWARD = "3"
RIGHT = "2"
LEFT = "4"
STOP = "0"
EXIT = "5"
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
    if (rightPower >= 0):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        motor1.start(abs(rightPower))
    elif (rightPower < 0):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        motor1.start(abs(rightPower))

    if (leftPower >= 0):
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
            motor2.start(abs(leftPower))
    elif (leftPower < 0):
            print('Backwards')
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
            motor2.start(abs(leftPower))
    
        
setup()
s = socket.socket()
hostname = "192.168.2.6"
port = 1234
s.connect((hostname, port))
print("Connected")
while(1):
    unpackedCommand = s.recv(struct.calcsize(INPUT_FORMAT))
    command = struct.unpack(INPUT_FORMAT, unpackedCommand)
    leftPower = command[0]
    rightPower = command[1]
    runMotors(leftPower, rightPower)
    '''leftPower = float(command[0])
    rightPower = float(command[1])
    runMotors(leftPower, rightPower)
    if (command == FORWARD):
        moveForward()
    elif(command == BACKWARD):
        moveBackward()
    elif(command == RIGHT):
        moveRight()
    elif(command == LEFT):
        moveLeft()
    elif(command == STOP):
        stop()
    elif(command == EXIT):
        s.close
        break
    '''    
        
GPIO.cleanup()



