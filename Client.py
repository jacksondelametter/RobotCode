import socket
import time

s = None
TIME_LIMIT = 1
previousTime = 0
currentTime = 0
def connect():
    global s
    global previousTime
    s = socket.socket()
    s.settimeout(1)
    hostname = "192.168.2.2"
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

connect()
while(1):
    try:
        command = s.recv(1024)
        currentTime = time.time()
        if ((currentTime - previousTime) > TIME_LIMIT):
            print("Timeout error")
            connect()
        elif(command == ""):
            print("Program Error")
            connect()
        previousTime = currentTime
        print(command)
    except KeyboardInterrupt:
        s.close
        break
    except:
        print('Program Error')
        s.close
        connect()
        
