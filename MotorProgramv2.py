import RPi.GPIO as GPIO
import time
import socket
import struct
import sys

ENA = 4
ENB = 27
IN1 = 17
IN2 = 18
IN3 = 22
IN4 = 23
motot1 = None
motor2 = None
s = None
previousTime = None

TIME_LIMIT = 1

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


def connect():
    global s
    global previousTime
    s = socket.socket()
    hostname = "192.168.2.3"
    port = 1234
    print("Connecting...")
    while(1):
        try:
            s.connect((hostname, port))
            previousTime = time.time()
            print('Connected')
            break
        except socket.error as e:
            print('Cant connect')
            s.close
        except KeyboardInterrupt:
            print("Program Ended")
            s.close
            sys.exit()

setup()
connect()
while(1):
    try:
        '''command = s.recv(1024)'''
        unpackedCommand = s.recv(struct.calcsize(INPUT_FORMAT))
        currentTime = time.time()
        if ((currentTime - previousTime) > TIME_LIMIT):
            print("Timeout error")
            connect()
        previousTime = currentTime
        command = struct.unpack(INPUT_FORMAT, unpackedCommand)
        print(command)
        leftPower = command[0]
        rightPower = command[1]
        runMotors(leftPower, rightPower) 
    except KeyboardInterrupt:
        print("Program Ended")
        GPIO.cleanup()
        s.close
        break
    except socket.error:
        print("Lost Connection")
        s.close
        runMotors(0, 0)
        connect()
    except:
        print("Program Error")
        s.close
        runMotors(0, 0)
        connect()
        



