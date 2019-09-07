import random
import socket

def socketGenerator(count):
    for i in range (count):
        yield socket.socket()

def generateRandomIPAddress() -> str:
    return "{0}.{1}.{2}.{3}".format(random.randint(1,255), random.randint(0,255),random.randint(0,255),random.randint(0,255))
