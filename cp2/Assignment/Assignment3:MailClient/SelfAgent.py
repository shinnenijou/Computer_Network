from socket import *
import account_config
import base64
import mysmtp

def extract_server(mail_addr):
    return mail_addr[mail_addr.find('@') + 1:]
def extract_extension(filename):
    return filename[filename.find('.') + 1:]

# Input a Server
serverName = input("Input Server Name: ")
serverPort = int(input("Input Server Port: "))
mailServer = (serverName, serverPort)

# SMTP message headers
fromMailAddr = input("Input MAIL FROM: ").strip()
USERNAME = account_config.ACCOUNTS[extract_server(fromMailAddr)][0]
PASSWORD = account_config.ACCOUNTS[extract_server(fromMailAddr)][1]
toMailAddr = input("Input RCPT TO: ").strip()
subject = input("Input mail subject: ").strip()

# Creat a smtp msg class
msg = mysmtp.SMTPMsg(fromMailAddr, toMailAddr)
msg.add_header("Subject", subject)
msg.add_type("multipart/mixed", "i7t8nfV3svUsjJ")

# Mail Content to send
text = input("Input mail contents to send(@text content or @file filename): ").strip()
text_beg = text.find("@text")
file_beg = text.find("@file")
files = text[file_beg:] if file_beg>text_beg else text[file_beg:text_beg]
text = text[text_beg:file_beg] if file_beg>text_beg else text[text_beg:]
# add text content
msg.add_boundary()
msg.add_type("text/plain")
msg.add_data(text[5:].strip().encode())
# add file content
for filename in files.strip().split()[1:]:
    with open(filename, "rb") as file:
        msg.add_boundary()
        msg.add_type(mysmtp.MIMA_TYPES[extract_extension(filename)])
        if extract_extension(filename) != "txt" or extract_extension(filename) != "html":
            msg.add_disposition("attachment", filename)
        msg.add_content_encoding("base64")
        msg.add_data(base64.b64encode(file.read()))
msg.add_end()

# Creat socket via SSL
clientSocket = mysmtp.SMTPSocket((serverName, serverPort))
clientSocket.connect()

# send HELO command
clientSocket.helo("Shinnen")

# send MAIL FROM conmand
# authenticate if required
if clientSocket.mail_from(fromMailAddr) != 250:
    clientSocket.login((USERNAME, PASSWORD))
    clientSocket.mail_from(fromMailAddr)

# send RECP TO conmand
clientSocket.rcpt_to(toMailAddr)

# send DATA command
if clientSocket.send_msg(msg) == 250:
    print(f"Successfully sent to {toMailAddr}.")

# Send QUIT command
clientSocket.quit()