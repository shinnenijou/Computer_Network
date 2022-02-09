from socket import *
serverName = "127.0.0.1" # localhost
#serverName = "1.117.32.175" # TenCent Cloud
serverPort = 1919 # self-defined port number

# create a socket object by socket.socket() 
# socket() function: return a socket object
# 1st param: domain type, 
#            "AF_INET" means IPv4, or 
#            "AF_INET6" means IPv6, or 
#            "AF_UNIX" means local host
# 2nd param: socket type, 
#           "SOCK_DGRAM" means UDP, or 
#           "SOCK_STREAM" means TCP, or 
#           "SOCK_RAW" means raw socket
# Since here we creat an UDP/IPv4 socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input("Input lowercase sentence:")

# Message should be sent by bytes, thus we use encode() method
# converting(coding) our string(message) to bytes, then pass bytes 
# to sento() method
# SocketClass.sento() method: no return
# 1st param: bytes to send
# 2dn param: must be tuple, including serverName and serverPort
clientSocket.sendto(message.encode(), (serverName, serverPort))

# SocketClass.recvfrom(): return the message received, and server information
# 1st param: receiving cache size
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print("From server: ", modifiedMessage.decode())

# SocketClass.close(): close the socket
clientSocket.close()