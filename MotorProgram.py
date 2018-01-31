import RPi.GPIO as GPIO
import time
import socket

ENA = 21
ENB = 16
IN1 = 2
IN2 = 15
IN3 = 23
IN4 = 25
motot1 = None
motor2 = None

FORWARD = "w"
BACKWARD = "s"
RIGHT = "d"
LEFT = "a"
STOP = "e"
EXIT = "r"

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
    motor1 = GPIO.PWM(ENA, 20000)
    motor2 = GPIO.PWM(ENB, 20000)

def moveForward():
    global motor1
    global motor2
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    motor1.start(75)
    motor2.start(75)

def moveBackward():
    global motor1
    global motor2
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    motor1.start(75)
    motor2.start(75)

def moveRight():
    global motor1
    global motor2
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    motor1.start(75)
    motor2.start(75)

def moveLeft():
    global motor1
    global motor2
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    motor1.start(75)
    motor2.start(75)
    
def stop():
    global motor1
    global motor2
    motor1.stop()
    motor2.stop()

def dualMotorTest():
    moveForward()
    time.sleep(3)
    stop()
    time.sleep(2)
    moveBackward()
    time.sleep(3)
    stop()
    time.sleep(2)
    moveRight()
    time.sleep(3)
    stop()
    time.sleep(2)
    moveLeft()
    time.sleep(3)
    stop()
    time.sleep(2)
    print("Test Complete")
setup()
s = socket.socket()
hostname = socket.gethostname()
port = 2225
s.connect((hostname, port))
while(1):
    command = s.recv(1024)
    if (command == FORWARD):
        moveForward()
        print("FORWARD")
    elif(command == BACKWARD):
        moveBackward()
        print("BACKWARD")
    elif(command == RIGHT):
        moveRight()
        print("RIGHT")
    elif(command == LEFT):
        moveLeft()
        print("LEFT")
    elif(command == STOP):
        stop()
        print("STOP")
    elif(command == EXIT):
        print("EXIT")
        s.close
        break
        
        
GPIO.cleanup()



