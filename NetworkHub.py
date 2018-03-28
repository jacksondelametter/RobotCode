import socket
import struct
from threading import Timer
import time

controllerSocket = None
networkHubSocket = None
motorServerSocket = None
servoServerSocket = None
motorSocket = None
servoSocket = None
INPUT_FORMAT = 'c i i'
MOTOR_FORMAT = 'i i'
SERVO_FORMAT = 'c h h'
'''MOTOR_OP_CODE = 0
SERVO_CONTROL_OP_COD = 2
SERVO_COMMAND_OP_CODE = 1'''
MOTOR_OP_CODE = 'm'
SERVO_CONTROL_OP_CODE = 'c'
SERVO_COMMAND_OP_CODE = 's'

def setupControllerConnection():
    global controllerSocket
    global networkHubSocket
    networkHubSocket = socket.socket()
    hostname = "192.168.2.2"
    port = 1234
    networkHubSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while(1):
        time.sleep(0.5)
        print('Creating network hub connection')
        try:
            networkHubSocket.bind((hostname, port))
            networkHubSocket.listen(100)
            print('Created network hub connection')
            break
        except:
            print('Couldnt create network hub connection')
    print('Created network hub connection')
    controllerSocket, addr = networkHubSocket.accept()
    print("Controller connected")
    

def setupMotorProgramConnection():
    global motorServerSocket
    global motorSocket
    motorServerSocket = socket.socket()
    hostname = socket.gethostname()
    port = 4001
    while(1):
        print('Waiting for motor program')
        try:
            motorServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            motorServerSocket.bind((hostname, port))
            motorServerSocket.listen(100)
            print("Created motor program connection")
            break
        except:
            print('Couldnt make motor program connection')
    motorSocket, addr = motorServerSocket.accept()

def setupServoProgramConnection():
    global servoServerSocket
    global servoSocket
    servoServerSocket = socket.socket()
    hostname = socket.gethostname()
    port = 2001
    while(1):
        print('Waiting for servo program')
        try:
            servoServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servoServerSocket.bind((hostname, port))
            servoServerSocket.listen(100)
            print("Created servo program connection")
            break
        except:
            print('Couldnt make servo program connection')
    servoSocket, addr = servoServerSocket.accept()

def sendMotorCommand(leftSpeed, rightSpeed):
    global motorSocket
    leftMotorSpeed = command[1]
    rightMotorSpeed = command[2]
    #print('Right motor speed: ' + str(rightSpeed) + 'Left motor speed' + str(leftSpeed))
    motorCommand = struct.pack(MOTOR_FORMAT, leftSpeed, rightSpeed)
    motorSocket.send(motorCommand)

def sendServoCommand(opCode, unpackedCommand):
    servoCommand = unpackedCommand[1]
    command = struct.pack(SERVO_FORMAT, opCode, servoCommand, 0)
    servoSocket.send(command)

def sendServoControl(opCode, unpackedCommand):
    servoChannel = unpackedCommand[1]
    servoPosition = unpackedCommand[2]
    command = struct.pack(SERVO_FORMAT, opCode, servoChannel, servoPosition)
    servoSocket.send(command)

def sendStopCommand():
    global controllerSocket
    print("Stopping")
    closeConnections()

def setupConnections():
    setupMotorProgramConnection()
    setupServoProgramConnection()
    setupControllerConnection()

def stopMotors():
    sendMotorCommand(0, 0)

def closeConnections():
    global networkHubSocket
    global controllerSocket
    global motorServerSocket
    global motorSocket
    global servoServerSocket
    global servoSocket
    try:
        networkHubSocket.shutdown(socket.SHUT_RDWR)
        networkHubSocket.close
    except:
        print('Controller socket already closed')
    try:
        controllerSocket.shutdown(socket.SHUT_RDWR)
        controllerSocket.close
    except:
        print('Controller socket already closed')
    '''try:
        motorSocket.shutdown(socket.SHUT_RDWR)
        motorSocket.close
    except:
        print('Motor socket already closed')
    try:
        servoSocket.shutdown(socket.SHUT_RDWR)
        servoSocket.close
    except:
        print('Servo socket already closed')
    try:
        motorServerSocket.shutdown(socket.SHUT_RDWR)
        motorServerSocket.close
    except:
        print('Motor server socket already closed')
    try:
        servoServerSocket.shutdown(socket.SHUT_RDWR)
        servoServerSocket.close
    except:
        print('Servo server socket already closed')'''


setupMotorProgramConnection()
setupServoProgramConnection()
#setupConnections()
setupControllerConnection()
while(1):
    try:
        timer = Timer(1, sendStopCommand)
        timer.start()
        print('Waiting for command...')
        packedCommand = controllerSocket.recv(struct.calcsize(INPUT_FORMAT))
        print('Received command')
        timer.cancel()
        command = struct.unpack(INPUT_FORMAT, packedCommand)
        opCode = command[0]
        #print('op code is ' + str(opCode))
        if(opCode == MOTOR_OP_CODE):
            print('Sending motor command')
            leftMotorSpeed = command[1]
            rightMotorSpeed = command[2]
            sendMotorCommand(leftMotorSpeed, rightMotorSpeed)
            continue
        elif(opCode == SERVO_COMMAND_OP_CODE):
            print('Sending servo command')
            sendServoCommand(opCode, command)
            continue
        elif(opCode == SERVO_CONTROL_OP_CODE):
            print('Sending servo control')
            sendServoControl(opCode, command)
            continue
    except KeyboardInterrupt:
        print("Program Ended")
        stopMotors()
        closeConnections()
        break
    except socket.error:
        print("Lost Connection")
        stopMotors()
        closeConnections()
        setupControllerConnection()
    except:
        print("Program Error")
        stopMotors()
        closeConnections()
        setupControllerConnection()

        
        
