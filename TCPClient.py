from socket import *

serverName = "127.0.0.1" # localhost
#serverName = "1.117.32.175" # TenCent Cloud
serverPort  = 1919
serverAddress = (serverName, serverPort)

# create a TCP/IPv4 socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# SocketClass.connect()method: create a TCP connection between client and server
# client will shake hand 3 times in the connection crearting process
# 1st param: must be tuple, including serverName and serverPort
clientSocket.connect(serverAddress)

message = input("Input lowercase sentence:")

# Since we have created a TCP connection between client and server
# we use send() method to send message instead of sendto()
# SocketClass.send()method: send message by TCP
# no need to pass serverAddress to the method
clientSocket.send(message.encode())

# Similarly, we use recv() method to receive the response from the server
# instead of recvfrom(), which is no need to pass serverAddress to the method
modifiedMessage = clientSocket.recv(2048)

print("From server: ", modifiedMessage.decode())
clientSocket.close()