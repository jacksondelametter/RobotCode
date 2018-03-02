#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

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
CHOOSE_MOTOR_COMMAND = 9
REST_ARM_COMMAND = 7
INITIATE_ARM_COMMAND = 8
STOP_COMMAND = 10
MOTOR_0 = 0
MOTOR_1 = 4
MOTOR_2 = 5
MOTOR_DELAY = 0.001

#gripper 330 closed- 230 open
'''def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 50                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)'''

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
    if(activeMotor == MOTOR_0):
        return currentPos0
    elif(activeMotor == MOTOR_1):
        return currentPos1
    elif(activeMotor == MOTOR_2):
        return currentPos2
    else:
        return -1

def setMotorPosition(activeMotor, position):
    global currentPos0
    global currentPos1
    global currentPos2
    if(activeMotor == MOTOR_0):
        currentPos0 = position
    elif(activeMotor == MOTOR_1):
        currentPos1 = position
    elif(activeMotor == MOTOR_2):
        currentPos2 = position
    else:
        print("Did not set position for motor")
    
def runMotorSlow(activeMotor, destinationValue):
    global motorPwm
    currentPos = getMotorPosition(activeMotor)
    if (currentPos == -1):
        print("Invalid active motor")
        return
    if(destinationValue >= 160 & destinationValue <= 500):
        incrementValue = 0
        if(currentPos >= destinationValue):
            incrementValue = -1
        elif(currentPos < destinationValue):
            incrementValue = 1
        for tick in range(currentPos, (destinationValue + incrementValue), incrementValue):
            print(tick)
            motorPwm.setPWM(activeMotor, 0, tick)
            time.sleep(MOTOR_DELAY)
        setMotorPosition(activeMotor, destinationValue)
    else:
        print('Bit value out of range in runMotorSlow')
    
def restArm():
    global currentPos0
    global currentPos1
    global currentPos2
    runMotor(MOTOR_0, 500)
    time.sleep(1.5)
    runMotor(MOTOR_1, 380)
    time.sleep(1.5)
    runMotor(MOTOR_2, 500)
    time.sleep(2)
    currentPos0 = 500
    currentPos1 = 380
    currentPos2 = 500
def initiateArm():
    runMotor(MOTOR_2, 500)
    time.sleep(1.5)
    runMotor(MOTOR_1, 200)
    time.sleep(1.5)
    runMotor(MOTOR_0, 450)
    time.sleep(1.5)

def stopMotors():
    runMotor(MOTOR_0, 0)
    runMotor(MOTOR_1, 0)
    runMotor(MOTOR_2, 0)

motorPwm = PWM(0x40)
motorPwm.setPWMFreq(50) # Set frequency to 50 Hz
restArm()
chooseMotor()
while True:
    try:
        command = input(activeMotor)
        if (command == CHOOSE_MOTOR_COMMAND):
            chooseMotor()
        elif (command == REST_ARM_COMMAND):
            restArm()
        elif (command == INITIATE_ARM_COMMAND):
            initiateArm()
        elif (command == STOP_COMMAND):
            stopMotors()
        else:
            runMotorSlow(activeMotor, command)
    except KeyboardInterrupt:
        stopMotors()
        break
