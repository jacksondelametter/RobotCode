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
currentPos3 = 0
currentPos4 = 0
CHOOSE_MOTOR_COMMAND = 'u'
REST_ARM_COMMAND = 'q'
INITIATE_ARM_COMMAND = 'w'
GRABBING_ARM_COMMAND = 'e'
PUT_IN_HOLE_COMMAND = 'r'
OPEN_CLOSE_GRIP_COMMAND = 't'
STOP_COMMAND = 'y'
INVALID_MOTOR = -1
MOTOR_0 = 0
MOTOR_1 = 4
MOTOR_2 = 5
MOTOR_3 = 6
MOTOR_4 = 7
MOTOR_DELAY = 0.0005
ARM_OPEN = True

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
    '''else:
        print('Bit value out of range in runMotor')'''

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
    global ARM_OPEN
    runMotorSlow(MOTOR_3, 160 - getMotorPosition(MOTOR_3))
    time.sleep(0.5)
    runMotorSlow(MOTOR_0, 320 - getMotorPosition(MOTOR_0))
    time.sleep(0.5)
    runMotorSlow(MOTOR_1, 500 - getMotorPosition(MOTOR_1))
    time.sleep(0.5)
    runMotorSlow(MOTOR_2, 280 - getMotorPosition(MOTOR_2))
    time.sleep(0.5)
    runMotorSlow(MOTOR_4, 330 - getMotorPosition(MOTOR_4))
    ARM_OPEN = False
    stopMotors()

def openCloseGrip():
    # Used for laying arm back down from arm ready position
    '''
    First motor1 to 360, motor2 to 300, motor0 to 500
    '''
    global ARM_OPEN
    if ARM_OPEN:
        runMotorSlow(MOTOR_4, 310 - getMotorPosition(MOTOR_4))
        time.sleep(0.5)
    else:
        # Arm is closed
        runMotorSlow(MOTOR_4, 230 - getMotorPosition(MOTOR_4))
        time.sleep(0.5)
        runMotor(MOTOR_4, 0)
    ARM_OPEN = not ARM_OPEN
    

def initialArmPos():
    # Used for initial arm position
    runMotor(MOTOR_0, 320)
    runMotor(MOTOR_1, 500)
    runMotor(MOTOR_2, 280)
    runMotor(MOTOR_3, 160)
    runMotor(MOTOR_4, 330)
    setMotorPosition(MOTOR_0, 320)
    setMotorPosition(MOTOR_1, 500)
    setMotorPosition(MOTOR_2, 280)
    setMotorPosition(MOTOR_3, 160)
    setMotorPosition(MOTOR_4, 330)
    
def initiateArm():
    '''
    First motor 1 to 230, motor 0 to 430, motor 2 to 300
    '''
    runMotorSlow(MOTOR_0, 360 - getMotorPosition(MOTOR_0))
    time.sleep(0.5)
    runMotorSlow(MOTOR_1, 160 - getMotorPosition(MOTOR_1))
    time.sleep(0.5)
    runMotorSlow(MOTOR_2, 350 - getMotorPosition(MOTOR_2))
    time.sleep(0.5)
    runMotorSlow(MOTOR_3, 500 - getMotorPosition(MOTOR_3))
    time.sleep(0.5)


def grabbingArm():
    # Used to grab block
    '''
    First motor2 to 500, motor1 to 160, motor0 to 480
    '''
    runMotorSlow(MOTOR_0, 280 - getMotorPosition(MOTOR_0))
    time.sleep(0.5)
    runMotorSlow(MOTOR_1, 250 - getMotorPosition(MOTOR_1))
    time.sleep(0.5)
    runMotorSlow(MOTOR_2, 500 - getMotorPosition(MOTOR_2))
    time.sleep(0.5)
    runMotorSlow(MOTOR_3, 320 - getMotorPosition(MOTOR_3))
    time.sleep(0.5)
    runMotorSlow(MOTOR_4, 230 - getMotorPosition(MOTOR_4))
        
def putInUpHole():
    # Used to put block into hole
    '''
    First motor0 to 480, motor1 to 200, motor2 to 480
    '''
    runMotorSlow(MOTOR_0, 480 - getMotorPosition(MOTOR_0))
    time.sleep(0.5)
    runMotorSlow(MOTOR_1, 210 - getMotorPosition(MOTOR_1))
    time.sleep(0.5)
    runMotorSlow(MOTOR_2, 480 - getMotorPosition(MOTOR_2))
    
def putInHole():
    runMotorSlow(MOTOR_0, 460 - getMotorPosition(MOTOR_0))
    time.sleep(0.5)
    runMotorSlow(MOTOR_1, 240 - getMotorPosition(MOTOR_1))
    time.sleep(0.5)
    runMotorSlow(MOTOR_2, 500 - getMotorPosition(MOTOR_2))
    time.sleep(0.5)

def putInDownHole():
    runMotorSlow(MOTOR_0, 400 - getMotorPosition(MOTOR_0))
    time.sleep(0.5)
    runMotorSlow(MOTOR_1, 270 - getMotorPosition(MOTOR_1))
    time.sleep(0.5)
    runMotorSlow(MOTOR_2, 430 - getMotorPosition(MOTOR_2))
    time.sleep(0.5)
    runMotorSlow(MOTOR_3, 395 - getMotorPosition(MOTOR_3))
    time.sleep(0.5)
    
motorPwm = PWM(0x40)
motorPwm.setPWMFreq(50) # Set frequency to 50 Hz
initialArmPos()
chooseMotor()
while True:
    try:
        command = raw_input(str(activeMotor) + ': ' + str(getMotorPosition(activeMotor)) + '- ')
        if (command == CHOOSE_MOTOR_COMMAND):
            chooseMotor()
        elif (command == REST_ARM_COMMAND):
            restArm()
        elif (command == INITIATE_ARM_COMMAND):
            initiateArm()
        elif (command == GRABBING_ARM_COMMAND):
            grabbingArm()
        elif(command == PUT_IN_HOLE_COMMAND):
            putInHole()
        elif(command == OPEN_CLOSE_GRIP_COMMAND):
            openCloseGrip()
        elif (command == STOP_COMMAND):
            stopMotors()
        else:
            runMotorSlow(activeMotor, int(command))
    except KeyboardInterrupt:
        stopMotors()
        break
