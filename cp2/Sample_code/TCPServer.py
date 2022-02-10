from multiprocessing import connection
from socket import *

serverPort = 1919
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))

# Let our socket start to listen connection request from clients
# SocketClass.listen()method
# 1st param: int, the maximal limit for the number of connections
# if the server is maintaining a connect with a client, other client
# must wait the server closing the existing conection to create a new 
# connection
serverSocket.listen(1)

print("The server is ready to receive")
while True:
    # SocketClass.accept()method: create a connection socket between 
    # the server and the client which shaked hand to the server
    connectionSocket, clientAddress = serverSocket.accept()
    print(f"Successfully created connection between {clientAddress[0]}:{clientAddress[1]}")
    massage = connectionSocket.recv(2048).decode()
    connectionSocket.send(massage.upper().encode())
    connectionSocket.close()