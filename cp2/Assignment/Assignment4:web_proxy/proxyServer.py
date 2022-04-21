from socket import *
import sys
import threading
from urllib import response

# if len(sys.argv) <= 2:
#     print('Uasge: "python3 ProcyServer.py [server_ip]" to start server')
#     sys.exit(2)


serverPort = 1919
serverAddr = ("", serverPort)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddr)
serverSocket.listen(10)

print("Ready to serve...")
while True:
    # Start receiving data from the client
    clientConnectionSocket, addr = serverSocket.accept()
    clientConnectionSocket.settimeout(5)
    print(f"Received a connection from: {addr[0]}:{addr[1]}")
    try:
        message = clientConnectionSocket.recv(2048).decode()
    except:
        clientConnectionSocket.close()
        continue
    if not message.split() or message.split()[0] != "GET":
        continue
    print(message)
    # Extract the filename from the given message
    filename = message.split()[1].partition('//')[2]
    hostname = message.split()[4].replace("www.", "", 1)
    #print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    #print(filetouse)
    try:
        # Check whether the file exist in the cache
        f = open(filename.replace('/', '_'), "rb")
        outputdata = f.read()
        fileExist = "true"
        # ProcyServer finds a cache hit and generates a response message
        sent_bytes = clientConnectionSocket.send(outputdata)
        if sent_bytes:
            f.close()
            print("Read from cache")
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Creat a socket on the proxyserver
            serverConnectionSocket = socket(AF_INET, SOCK_STREAM)
            try:
                # Connect to the socket to port 80
                serverConnectionSocket.connect((hostname, 80))
                # Create a tempory file on this socket and ask port 80
                # for the file requested by the client
                # read the response into buffer
                fileobj = serverConnectionSocket.makefile("rwb", 0)
                fileobj.write(f"GET http://{filename} HTTP/1.1\r\n".encode())
                fileobj.write(f"Host: {hostname}\r\n".encode())
                fileobj.write(f"Connection: close\r\n\r\n".encode())
                response = b""
                bodyLength = -2 # "\r\n"
                isLength = False
                isChunked = False
                for line in fileobj:
                    response += line
                    # if message ended by length
                    if not isLength and not isChunked \
                       and line.decode().split() \
                       and line.decode().split()[0] == "Content-Length:":
                        isLength = True
                        contentLength = int(line.decode().split()[1])
                    # if message ended by chunked
                    if not isLength and not isChunked \
                       and line.decode().split() \
                       and line.decode().split()[1] == "chunked":
                        isChunked = True
                    if isLength and (bodyLength != -2 or line == b"\r\n"):
                        bodyLength += len(line)
                    if (isChunked and line == b"0\r\n") \
                        or (isLength and bodyLength == contentLength):
                        break
                fileobj.close()
                #print(response.decode())
                # Creat a new file in the cache for the requested file
                # Also send the response in the buffer to client socket
                tmpFile = open(filename.replace('/', '_'), "wb")
                tmpFile.write(response)
                tmpFile.close()
                serverConnectionSocket.close()
                clientConnectionSocket.send(response)
            except TimeoutError:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            clientConnectionSocket.send("HTTP/1.0 404 NOTFOUND\r\n".encode())
    clientConnectionSocket.close()