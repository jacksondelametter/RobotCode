#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import socket
import struct

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 160  # Min pulse length out of 4096
servoMax = 500  # Max pulse length out of 4096
servoNeutral = 320
activeMotor = 0
currentPos0 = 0
currentPos1 = 0
currentPos2 = 0
currentPos3 = 0
currentPos4 = 0

INVALID_MOTOR = -1
MOTOR_0 = 0
MOTOR_1 = 4
MOTOR_2 = 5
MOTOR_3 = 6
MOTOR_4 = 7
MOTOR_DELAY = 0.0005
networkHubSocket = None

#Commands
CHOOSE_MOTOR_COMMAND = 9
REST_ARM_COMMAND = 0
INITIATE_ARM_COMMAND = 1
GRABBING_ARM_COMMAND = 2
IN_HOLE_COMMAND = 3
STOP_COMMAND = 4
SERVO_FORMAT = 'c h h'
SERVO_COMMAND = 's'
SERVO_CONTROL = 'c'

#gripper 330 closed- 230 open

def chooseMotor():
    global activeMotor
    motorNum = input('Choose Motor')
    if(motorNum == MOTOR_0):
        activeMotor = motorNum
    elif(motorNum == MOTOR_1):
        activeMotor = motorNum
    elif(motorNum == MOTOR_2):
        activeMotor = motorNum
    elif(motorNum == MOTOR_3):
        activeMotor = motorNum
    elif(motorNum == MOTOR_4):
        activeMotor = motorNum
    else:
        activeMotor = MOTOR_0

def runMotor(activeMotor, bit):
    global motorPwm
    if(bit >= 160 & bit <= 500):
        motorPwm.setPWM(activeMotor, 0, bit)
    else:
        print('Bit value out of range in runMotorSlow')

def getMotorPosition(activeMotor):
    global currentPos0
    global currentPos1
    global currentPos2
    global currentPos3
    global currentPos4
    if(activeMotor == MOTOR_0):
        return currentPos0
    elif(activeMotor == MOTOR_1):
        return currentPos1
    elif(activeMotor == MOTOR_2):
        return currentPos2
    elif(activeMotor == MOTOR_3):
        return currentPos3
    elif(activeMotor == MOTOR_4):
        return currentPos4
    else:
        return INVALID_MOTOR

def setMotorPosition(activeMotor, position):
    global currentPos0
    global currentPos1
    global currentPos2
    global currentPos3
    global currentPos4
    if(activeMotor == MOTOR_0):
        currentPos0 = position
    elif(activeMotor == MOTOR_1):
        currentPos1 = position
    elif(activeMotor == MOTOR_2):
        currentPos2 = position
    elif(activeMotor == MOTOR_3):
        currentPos3 = position
    elif(activeMotor == MOTOR_4):
        currentPos4 = position
    else:
        print("Did not set position for motor")
    
def runMotorSlow(activeMotor, incrementPos):
    global motorPwm
    currentPos = getMotorPosition(activeMotor)
    destinationValue = currentPos + incrementPos
    #print('Destination value is ' + str(destinationValue))
    if (currentPos == INVALID_MOTOR):
        print("Invalid active motor")
        return
    if(activeMotor == MOTOR_4 and destinationValue <= 230):
        # motor 4 is lower than 230
        destinationValue = 230
    elif(activeMotor == MOTOR_4 and destinationValue >= 330):
        # motor 4 is higher than 330
        destinationValue = 330
    elif(destinationValue <= 160):
        # motor is lower than 160
        destinationValue = 160
    elif(destinationValue >= 500):
        # motor is higher than 500
        destinationValue = 500
    incrementValue = 0
    if(currentPos >= destinationValue):
        incrementValue = -1
    elif(currentPos < destinationValue):
        incrementValue = 1
    for tick in range(currentPos, (destinationValue + incrementValue), incrementValue):
        #print(tick)
        motorPwm.setPWM(activeMotor, 0, tick)
        time.sleep(MOTOR_DELAY)
    setMotorPosition(activeMotor, destinationValue)
    #print('Motor' + str(activeMotor) + ': ' + str(getMotorPosition(activeMotor)))

def stopMotors():
    runMotor(MOTOR_0, 0)
    runMotor(MOTOR_1, 0)
    runMotor(MOTOR_2, 0)
    runMotor(MOTOR_3, 0)
    runMotor(MOTOR_4, 0)
    print('Motors stopped')


def restArm():
    # Used for laying arm back down from arm ready position
    '''
    First motor1 to 360, motor2 to 300, motor0 to 500
    '''
    runMotorSlow(MOTOR_4, 330 - getMotorPosition(MOTOR_4))
    time.sleep(0.5)
    runMotorSlow(MOTOR_3, 320 - getMotorPosition(MOTOR_3))
    time.sleep(0.5)
    runMotorSlow(MOTOR_1, 360 - getMotorPosition(MOTOR_1))
    time.sleep(0.5)
    runMotorSlow(MOTOR_2, 300 - getMotorPosition(MOTOR_2))
    time.sleep(0.5)
    runMotorSlow(MOTOR_0, 500 - getMotorPosition(MOTOR_0))
    stopMotors()

def initiateArm():
    '''
    First motor 1 to 230, motor 0 to 430, motor 2 to 300
    '''
    runMotorSlow(MOTOR_3, 320 - getMotorPosition(MOTOR_3))
    time.sleep(0.5)
    runMotorSlow(MOTOR_4, 330 - getMotorPosition(MOTOR_4))
    time.sleep(0.5)
    runMotorSlow(MOTOR_1, 230 - getMotorPosition(MOTOR_1))
    time.sleep(1)
    runMotorSlow(MOTOR_0, 430 - getMotorPosition(MOTOR_0))
    time.sleep(1)
    runMotorSlow(MOTOR_2, 300 - getMotorPosition(MOTOR_2))
    time.sleep(1)

def initialArmPos():
    # Used for initial arm position
    runMotor(MOTOR_0, 500)
    runMotor(MOTOR_1, 360)
    runMotor(MOTOR_2, 300)
    runMotor(MOTOR_3, 320)
    runMotor(MOTOR_4, 330)
    setMotorPosition(MOTOR_0, 500)
    setMotorPosition(MOTOR_1, 360)
    setMotorPosition(MOTOR_2, 300)
    setMotorPosition(MOTOR_3, 320)
    setMotorPosition(MOTOR_4, 330)

def grabbingArm():
    # Used to grab block
    '''
    First motor2 to 500, motor1 to 160, motor0 to 480
    '''
    runMotorSlow(MOTOR_2, 500 - getMotorPosition(MOTOR_2))
    time.sleep(0.5)
    runMotorSlow(MOTOR_1, 160 - getMotorPosition(MOTOR_1))
    time.sleep(0.5)
    runMotorSlow(MOTOR_0, 480 - getMotorPosition(MOTOR_0))
    time.sleep(0.5)
    runMotorSlow(MOTOR_4, 230 - getMotorPosition(MOTOR_4))
        
def putInHole():
    # Used to put block into hole
    '''
    First motor0 to 480, motor1 to 200, motor2 to 480
    '''
    runMotorSlow(MOTOR_0, 480 - getMotorPosition(MOTOR_0))
    time.sleep(0.5)
    runMotorSlow(MOTOR_1, 210 - getMotorPosition(MOTOR_1))
    time.sleep(0.5)
    runMotorSlow(MOTOR_2, 480 - getMotorPosition(MOTOR_2))

def connectToNetworkHub():
    global networkHubSocket
    global previousTime
    networkHubSocket = socket.socket()
    hostname = socket.gethostname()
    port = 2001
    print("Connecting to network hub")
    networkHubSocket.connect((hostname, port))
    print("Connected to network hub")

connectToNetworkHub()
motorPwm = PWM(0x40)
motorPwm.setPWMFreq(50) # Set frequency to 50 Hz
initialArmPos()
while(1):
    try:
        packedCommand = networkHubSocket.recv(struct.calcsize(SERVO_FORMAT))
        command = struct.unpack(SERVO_FORMAT, packedCommand)
        opCode = command[0]
        print(command)
        if(opCode == SERVO_COMMAND):
            servoCommand = command[1]
            if (servoCommand == REST_ARM_COMMAND):
                print('Resting arm')
                restArm()
            elif (servoCommand == INITIATE_ARM_COMMAND):
                print('Initiating arm')
                initiateArm()
            elif (servoCommand == GRABBING_ARM_COMMAND):
                print('Arm ready to grab')
                grabbingArm()
            elif (servoCommand == IN_HOLE_COMMAND):
                print("Ready to put in hole")
            elif (servoCommand == STOP_COMMAND):
                print('Servo motors stopped')
                stopMotors()
        elif(opCode == SERVO_CONTROL):
            servoChannel = command[1]
            servoPosition = command[2]
            print('Controlling servo ' + str(servoChannel) + ' at position ' + str(servoPosition))
            runMotorSlow(servoChannel, servoPosition)
    except KeyboardInterrupt:
        stopMotors()
        break
