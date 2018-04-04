import time
import socket
import struct

motorServerSocket = None
motorSocket = None

def setupMotorProgramConnection():
    global motorServerSocket
    global motorSocket
    motorServerSocket = socket.socket()
    hostname = socket.gethostname()
    port = 4002
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
    print('Connected to motor program')

setupMotorProgramConnection()
while(1):
    try:
        print('waiting')
        time.sleep(2)
        packedCommand = struct.pack('? ? ? ?', True, True, True, False)
        print('Sending automation status')
        motorSocket.send(packedCommand)
    except KeyboardInterrupt:
        break
    except:
        print('Program Error')
        continue
