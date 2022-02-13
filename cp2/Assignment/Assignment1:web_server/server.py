from socket import *
from time import *
from connectionThread import *

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = 80
    serverSocket.bind(("", serverPort))
    serverSocket.listen()
    print("The server is ready to receive")

    while True:
        connection = ConnectionThread(serverSocket.accept())
        connection.start()
    
    serverSocket.close()

if __name__ == "__main__":
    main()