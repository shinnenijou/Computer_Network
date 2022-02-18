from socket import *
import account_config
import base64
import ssl

def send_n_recv(socket, bytes):
    socket.send(bytes)
    recv = socket.recv(1024).decode()
    print(f"Server: {recv}")
    return recv

def authenticate(socket, username, password):
    print("Client: AUTH LOGIN")
    send_n_recv(socket ,"AUTH LOGIN\r\n".encode())
    print("Client:", username)
    send_n_recv(socket, base64.b64encode(username.encode()) + b"\r\n")
    print("Client:", password)
    send_n_recv(socket, base64.b64encode(password.encode()) + b"\r\n")

MSG = "From: test1@163.com\r\n" \
    + "To: test2@pku.edu.cn\r\n" \
    + "Subject: SMTP\r\n" \
    + "\r\n" \
    + "Hello"

USERNAME = account_config.ACCOUNTS["163.com"][0]
PASSWORD = account_config.ACCOUNTS["163.com"][1]
ENDMSG = "\r\n.\r\n"
# Choose a mail server
serverName = "smtp.163.com"
serverPort = 465
mailServer = (serverName, serverPort)
# Creat socket via SSL
# ssl.creat_default_context() return a default SSL context
SSLContext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
# SSLContext.wrap_socket() wrap a normal socket into SSL socket
clientSSLSocket = SSLContext.wrap_socket(socket(AF_INET, SOCK_STREAM), 
                                         server_hostname=serverName)
clientSSLSocket.connect(mailServer)

# receive msg from mail server
recv = clientSSLSocket.recv(1024).decode()
print(f"Server: {recv}")

# send HELO command
# EHLO in SMTP-AUTH
cmd = "EHLO shinnen.cloud\r\n"
print(f"Client: {cmd}")
recv = send_n_recv(clientSSLSocket, cmd.encode())

# SMTP-AUTH
authenticate(clientSSLSocket, USERNAME, PASSWORD)

# send MAIL FROM conmand
cmd = "MAIL FROM: <littlesword111@163.com>\r\n"
print(f"Client: {cmd}")
recv = send_n_recv(clientSSLSocket, cmd.encode())

# send RECP TP conmand
cmd = "RCPT TO: <1300011717@pku.edu.cn>\r\n"
print(f"Client: {cmd}")
recv = send_n_recv(clientSSLSocket, cmd.encode())

# send DATA command
cmd = "DATA\r\n"
print(f"Client: {cmd}")
recv = send_n_recv(clientSSLSocket, cmd.encode())

# send message data
print("Client:")
print(f"{MSG}")
clientSSLSocket.send(MSG.encode())

# message ends with a single period
print(f"Client: {ENDMSG.strip()}")
recv = send_n_recv(clientSSLSocket, ENDMSG.encode())

# Send QUIT command
cmd = "QUIT\r\n"
print(f"Client: {cmd}")
recv = send_n_recv(clientSSLSocket, cmd.encode())

clientSSLSocket.close()