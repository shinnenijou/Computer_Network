from socket import *
import sys

def main():
    if(len(sys.argv) < 4):
        return
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
    serverAddr = (serverName, serverPort)
    filename = sys.argv[3]

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(serverAddr)
    request_line = f"GET {filename} HTTP/1.1\r\n\r\n"
    clientSocket.send(request_line.encode())
    response = 1
    # 使用循环来接受传输的报文以确保报文能够传输完全（也保证服务器不会阻塞）
    while response:
        response = clientSocket.recv(2048).decode()
        print(response, end = "")
    clientSocket.close()
    

if __name__ == "__main__":
    main()