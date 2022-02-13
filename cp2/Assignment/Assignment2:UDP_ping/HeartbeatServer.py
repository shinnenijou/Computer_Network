from socket import *

# CONSTANT
HEARTBEAT_INTERVAL = 2
MAX_MISSING = 5

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(("", 1919))
# Set timeout for the socket
# if heartbeat packet is missing more than this limit
# we consider the client is stopped
serverSocket.settimeout(HEARTBEAT_INTERVAL + 1)

# Receive the first heartbeat
while True:
    try:
        heartbeat, address = serverSocket.recvfrom(1024)
        heartbeat = heartbeat.decode().split()
        heartbeatID = int(heartbeat[0])
        heartbeatTime = float(heartbeat[1])
        prevHeartbeatTime = heartbeatTime
        print(f"Receive the first heartbeat from {heartbeatID}")
        break
    except timeout:
        pass

missingCount = 0
# Receive the sequential heartbeat
while True:
    try:
        # Receive the client packet along with the address it is coming from
        heartbeat, address = serverSocket.recvfrom(1024)
        # Reset missing count if receive successfully
        missingCount = 0
        # read the sequence number and timestamp from the packet
        heartbeat = heartbeat.decode().split()
        heartbeatID = int(heartbeat[0])
        heartbeatTime = float(heartbeat[1])
        print(f"Time from previous heartbeat: {heartbeatTime - prevHeartbeatTime}")
        prevHeartbeatTime = heartbeatTime
    except timeout:
        # Increase missing count
        missingCount += 1
        print("Heatbeat is missing")
    if missingCount >= MAX_MISSING:
        break

print("Client is stopped")