import time
import threading

class ConnectionThread(threading.Thread):
    def __init__(self, tuple):
        threading.Thread.__init__(self)
        self.connectionSocket = tuple[0]
        self.addr = tuple[1]
        print(f"Successfully connected @{self.addr[0]}:{self.addr[1]}", end = ", ")
        print(f"current total connections: {threading.active_count()}")

    def run(self):
        message = self.connectionSocket.recv(2048)
        response(self.connectionSocket, self.addr, message)

def response(connectionSocket, addr, message):
    try:
        # HTTP REQUEST LINE
        # {REQUEST_TYPE} {REQUEST_URL} {HTTP_VERSION}
        filename = message.split()[1]
        f = open(filename[1:])
        file = f.read()
        f.close()
        # Send one HTTP HEADER LINE
        # {HTTP_VERSION} {STATUS_CODE} OK
        headerLine = ["HTTP/1.1 200 OK\r\n"]
        headerLine.append("Connection: close\r\n")
        headerLine.append(f"Date: {time.asctime(time.gmtime(time.time()))}\r\n")
        headerLine.append(f"Content-Length: {len(file)}\r\n")
        headerLine.append(f"Content-Type: text/html\r\n")
        headerLine.append("\r\n")
        outputdata = ""
        for line in headerLine:
            outputdata += line
        outputdata += file
        # Send the content of the request
        # two ways to send message to TCP
        # 1. send char one by one
        # 2. send whole message at once
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        #connectionSocket.send(outputdata.encode())

        # Close TCP connection
        connectionSocket.close()
        print(f"Connection closed @{addr[0]}:{addr[1]}")
    except IOError:
        print("File NOT FOUND")
        outputdata = "HTTP/1.1 404 NOTFOUND\r\n\r\n"
        # Send response message for file not found
        # two ways to send message to TCP
        # 1. send char one by one
        # 2. send whole message at once
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        #connectionSocket.send(outputdata)
        print(f"Connection closed @{addr[0]}:{addr[1]}")
        connectionSocket.close()