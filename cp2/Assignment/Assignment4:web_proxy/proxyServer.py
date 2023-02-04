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

while True:
    # Start receiving data from the client
    print("Ready to serve...")
    clientConnectionSocket, addr = serverSocket.accept()
    clientConnectionSocket.settimeout(5)
    print(f"Received a connection from: {addr[0]}:{addr[1]}")
    message = clientConnectionSocket.recv(2048).decode()
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    if filename[-3:] == "ico":
        continue
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:].replace('/', '_'), "r")
        outputdata = f.readlines()
        f.close()
        fileExist = "true"
        # ProcyServer finds a cache hit and generates a response message
        clientConnectionSocket.send("HTTP1.0 200 OK\r\n".encode())
        clientConnectionSocket.send("Content-Type: text/html\r\n".encode())
        contentLength = 0
        content = ""
        for line in outputdata:
            contentLength += len((line + "\r\n").encode())
            content += line + "\r\n"
        clientConnectionSocket.send(f"Content-Length: {contentLength}\r\n".encode())
        clientConnectionSocket.send("\r\n".encode())
        clientConnectionSocket.send(content.encode())
        print("Read from cache")
    # Error handling for file not found in cache
    except IOError:
        # exception maybe occur by other error but not FileNotFound
        if fileExist == "false":
            # Creat a socket on the proxyserver
            serverConnectionSocket = socket(AF_INET, SOCK_STREAM)
            hostname = filename.replace("www.", "", 1 ).partition("/")[0]
            try:
                # Connect to the socket to port 80
                print(hostname)
                serverConnectionSocket.connect((hostname, 80))
                # Create a tempory file on this socket and ask port 80
                # for the file requested by the client
                # read the response into buffer
                fileobj = serverConnectionSocket.makefile("w")
                fileobj.write(f"GET /{filename.partition('/')[2]} HTTP/1.0\r\n")
                fileobj.write(f"Host: {filename.partition('/')[0]}\r\n\r\n")
                fileobj.close()
                # read the reponse into buffer
                fileobj = serverConnectionSocket.makefile("r")
                resp_line = "init"
                resp_body = ""
                first_rn = True
                # read header
                while resp_line:
                    resp_line = fileobj.readline()
                    resp_body += resp_line
                    if first_rn and not resp_line.strip():
                        resp_body = ""
                        first_rn = False
                # read body
                fileobj.close()
                #print(response.decode())
                # Creat a new file in the cache for the requested file
                # Also send the response in the buffer to client socket
                tmpFile = open(f"./{filename.replace('/', '_')}", "w")
                tmpFile.write(resp_body)
                tmpFile.close()
                serverConnectionSocket.close()
                clientConnectionSocket.send("HTTP1.0 200 OK\r\n".encode())
                clientConnectionSocket.send("Content-Type: text/html\r\n".encode())
                contentLength = 0
                content = ""
                for line in resp_body:
                    contentLength += len((line + "\r\n").encode())
                    content += line + "\r\n"
                clientConnectionSocket.send(f"Content-Length: {contentLength}\r\n".encode())
                clientConnectionSocket.send("\r\n".encode())
                clientConnectionSocket.send(resp_body.encode())
            except TimeoutError:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            clientConnectionSocket.send("HTTP/1.0 404 NOTFOUND\r\n".encode())
    clientConnectionSocket.close()