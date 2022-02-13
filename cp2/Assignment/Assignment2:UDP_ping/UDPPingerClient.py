from socket import *
import time

# Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number of server to ping
serverAddr = ("1.117.32.175", 1919) # TenCent Cloud
#serverAddr = ("127.0.0.1", 1919) # Localhost
# Set 1 second timeout for the socket
clientSocket.settimeout(1)
# Set Ping times
pingTimes = 10
RTTs = []
# Ping the server for 10 times
for i in range(pingTimes):
    print(f"Ping {i+1} {time.asctime(time.localtime())}", end = " ")
    sndpkt = "hello".encode()
    time_send = time.time()
    clientSocket.sendto(sndpkt, serverAddr)
    try:
        message, addr = clientSocket.recvfrom(1024)
        time_recv = time.time()
        RTTs.append(time_recv - time_send)
        print(message.decode(), f"RTT: {time_recv - time_send}")
    except timeout:
        RTTs.append(-1)
        print("Request timed out")
print("Ping ended")
# Process RTT data
sum, cnt, min, max = 0, 0, 2, -1
for t in RTTs:
    if t > 0:
        sum += t
        cnt += 1
        if t > max:
            max = t
        elif t < min:
            min = t
print(f"MaxRTT: {max}, MinRTT: {min},\
    AvgRTT: {sum/cnt}, LossRate: {1-cnt/pingTimes}")
