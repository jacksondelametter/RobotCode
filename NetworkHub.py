import socket
import struct
from threading import Timer

controllerSocket = None
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

def connectToController():
    global controllerSocket
    controllerSocket = socket.socket()
    hostname = "192.168.2.3"
    port = 1234
    while(1):
        print("Connecting to controller")
        try:
            controllerSocket.connect((hostname, port))
            print('Connected to controller')
            break
        except socket.error as e:
            print('Cant connect to controller')
            controllerSocket.close
        except KeyboardInterrupt:
            print("Program Ended")
            controllerSocket.close
            sys.exit()

def setupMotorProgramConnection():
    global motorServerSocket
    global motorSocket
    motorServerSocket = socket.socket()
    hostname = socket.gethostname()
    port = 4001
    motorServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    motorServerSocket.bind((hostname, port))
    motorServerSocket.listen(100)
    print('Waiting for motor program')
    motorSocket, addr = motorServerSocket.accept()
    print("Motor program connected")

def setupServoProgramConnection():
    global servoServerSocket
    global servoSocket
    servoServerSocket = socket.socket()
    hostname = socket.gethostname()
    port = 2001
    servoServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servoServerSocket.bind((hostname, port))
    servoServerSocket.listen(100)
    print('Waiting for servo program')
    servoSocket, addr = servoServerSocket.accept()
    print("Servo program connected")

def sendMotorCommand(unpackedCommand):
    global motorSocket
    leftMotorSpeed = command[1]
    rightMotorSpeed = command[2]
    motorCommand = struct.pack(MOTOR_FORMAT, leftMotorSpeed, rightMotorSpeed)
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
    controllerSocket.shutdown(socket.SHUT_RDWR)
    controllerSocket.close
    
connectToController()
setupMotorProgramConnection()
setupServoProgramConnection()
while(1):
    try:
        #timer = Timer(3, sendStopCommand)
        #timer.start()
        #print('Waiting for command...')
        packedCommand = controllerSocket.recv(struct.calcsize(INPUT_FORMAT))
        #print('Received command')
        #timer.cancel()
        #controllerSocket.send("H")
        command = struct.unpack(INPUT_FORMAT, packedCommand)
        opCode = command[0]
        #print('op code is ' + str(opCode))
        if(opCode == MOTOR_OP_CODE):
            print('Sending motor command')
            sendMotorCommand(command)
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
        GPIO.cleanup()
        controllerSocket.close
        break
    except socket.error:
        print("Lost Connection")
        controllerSocket.close
        connectToController()
    except:
        print("Program Error")
        controllerSocket.close
        connectToController()
        
        
