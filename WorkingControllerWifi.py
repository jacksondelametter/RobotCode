import socket
import pygame

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()



s = socket.socket()
hostname = socket.gethostname()
port = 2228
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((hostname, port))
s.listen(5)
print("Running")

c, addr = s.accept()
print("Got connection")
try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.5:
                        c.send("4".encode("utf-8"))
                        print("left")
                    if event.value > 0.5:
                        c.send("2".encode("utf-8"))
                        print("right")
                elif event.axis == 1:
                    if event.value < -0.5:
                        c.send("1".encode("utf-8"))
                        print("up")
                    if event.value > 0.5:
                        c.send("3".encode("utf-8"))
                        print("down")
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 2:
                    c.send("0".encode("utf-8"))
                    print("stop")
                elif event.button == 3:
                    c.send("5".encode("utf-8"))
                    print("Closing")
                    s.close
                    c.close
                    break
except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()
