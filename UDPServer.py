from socket import *

serverPort = 1919
serverSocket = socket(AF_INET, SOCK_DGRAM)

# SocketClass.bind()method: by binding the port number and socket, 
# any message sent to this port will be lead to our socket
# 1st param: must be tuple, including serverName and serverPort
# which empty string means localhost
serverSocket.bind(("", serverPort))
print("The server is ready to receive")
while True:
    message , clientAddress = serverSocket.recvfrom(2048)
    print(f"succefully received message from {clientAddress[0]}:{clientAddress[1]}")
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)