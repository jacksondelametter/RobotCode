import socket

s = socket.socket()
hostname = socket.gethostname()
port = 2225
s.bind((hostname, port))
s.listen(5)

c, addr = s.accept()
print("Got connection")
while(1):
    command = raw_input(">")
    c.send(command)
    if(command == "r"):
        s.close
        c.close
        break

    
    
