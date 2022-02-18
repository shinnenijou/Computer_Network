import threading
from socket import *

def recvFromTCP(serverSocket):
    connectionSocket, addr = serverSocket.accept()
    print(f"Connected with {addr[0]}:{addr[1]}")
    message = connectionSocket.recv(2048)
    print(message.decode())
    connectionSocket.close()

serverPort = 1919
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

while True:
    thread = threading.Thread(target=recvFromTCP, args=(serverSocket,))
    thread.start()