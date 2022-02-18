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
def extract_server(mail_addr):
    return mail_addr[mail_addr.find('@') + 1:]

# Input a Server
serverName = input("Server Name: ")
serverPort = int(input("Server Port: "))
mailServer = (serverName, serverPort)

# SMTP message headers
mail_from = input("MAIL FROM: ").strip()
USERNAME = account_config.ACCOUNTS[extract_server(mail_from)][0]
PASSWORD = account_config.ACCOUNTS[extract_server(mail_from)][1]
rcpt_to = input("RCPT TO: ").strip()
subject = input("Input mail subject: ").strip()

# Mail Content to send
content = input("Input mail contents to send(or @file filename): ").strip()
if content[:5] == "@file":
    with open(content.split()[1], "rb") as file:
        content = file.read()
else:
    content = content.encode()

# Creat socket via SSL
# ssl.creat_default_context() return a default SSL context
SSLContext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
# SSLContext.wrap_socket() wrap a normal socket into SSL socket
clientSSLSocket = SSLContext.wrap_socket(socket(AF_INET, SOCK_STREAM), 
                                         server_hostname=serverName)
clientSSLSocket.connect(mailServer)

# receive msg from mail server
recv = clientSSLSocket.recv(1024).decode()
print(f"Server: {recv}".strip())

# send HELO command
cmd = "EHLO shinnen.cloud\r\n"
print("Client:", cmd.strip())
recv = send_n_recv(clientSSLSocket, cmd.encode())

# send MAIL FROM conmand
while True:
    cmd = f"MAIL FROM: <{mail_from}>\r\n"
    print(f"Client: {cmd}".strip())
    recv = send_n_recv(clientSSLSocket, cmd.encode())
    # If not required authentication
    if recv[:3] == "250":
        break
    # If required authentication
    elif recv[:2] == "55":
        authenticate(clientSSLSocket, USERNAME, PASSWORD)

# send RECP TP conmand
cmd = f"RCPT TO: <{rcpt_to}>\r\n"
print("Client:", cmd.strip())
recv = send_n_recv(clientSSLSocket, cmd.encode())

# send DATA command
cmd = "DATA\r\n"
print("Client:", cmd.strip())
recv = send_n_recv(clientSSLSocket, cmd.encode())

# send message data
headers = f"From: {mail_from}\r\n" \
    + f"To: {rcpt_to}\r\n" \
    + f"Subject: {subject}\r\n" \
    + "\r\n" 
print("Client:")
print(f"{headers}", end = "")
clientSSLSocket.send(headers.encode())
print(content.decode())
clientSSLSocket.send(content)

# message ends with a single period
cmd = "\r\n.\r\n"
print("Client:", cmd.strip())
recv = send_n_recv(clientSSLSocket, cmd.encode())

# Send QUIT command
cmd = "QUIT\r\n"
print("Client:", cmd.strip())
recv = send_n_recv(clientSSLSocket, cmd.encode())

clientSSLSocket.close()