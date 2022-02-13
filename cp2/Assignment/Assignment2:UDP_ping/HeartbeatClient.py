from socket import *
from sys import byteorder
import time
import ctypes

# CONSTANT
CLIENT_ID = 1
HEARTBEAT_INTERVAL = 2

# Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number of server to ping
#serverAddr = ("1.117.32.175", 1919) # TenCent Cloud
serverAddr = ("127.0.0.1", 1919) # Localhost

# Continuously send heartbeat packet to server
while True:
    message = f"{CLIENT_ID} {time.time()}"
    clientSocket.sendto(message.encode(), serverAddr)
    time.sleep(HEARTBEAT_INTERVAL)