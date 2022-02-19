from socket import *
import base64
import ssl

class SMTPSocket():

    def __init__(self, tuple) -> None:
        self.serverAddr = tuple
        self._SSLContext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
        self._SSLSocket = self._SSLContext.wrap_socket(socket(AF_INET, SOCK_STREAM), 
            server_hostname=self.serverAddr[0])

    def connect(self) -> int:
        self._SSLSocket.connect(self.serverAddr)
        recv = self._SSLSocket.recv(1024)
        return int(recv[:3])

    def helo(self, hostname="") -> int:
        command = "EHLO " + hostname
        recv = self._send_n_recv(command.encode() + b"\r\n")
        return int(recv[:3])

    def mail_from(self, mailAddr) -> int:
        command = f"MAIL FROM: <{mailAddr}>"
        recv = self._send_n_recv(command.encode() + b"\r\n")
        return int(recv[:3])

    def rcpt_to(self, mailAddr) -> int:
        command = f"RCPT TO: <{mailAddr}>"
        recv = self._send_n_recv(command.encode() + b"\r\n")
        return int(recv[:3])

    def send_msg(self, SMTPMsg) -> int:
        command = "DATA"
        recv = self._send_n_recv(command.encode() + b"\r\n")
        # EXCEPTION
        if recv[:3] != "354":
            raise IOError
        recv = self._send_n_recv(SMTPMsg.encode() + b"\r\n.\r\n")
        return int(recv[:3])

    def login(self, tuple) -> int:
        user = tuple[0]
        password = tuple[1]
        command = "AUTH LOGIN"
        recv = self._send_n_recv(command.encode() + b"\r\n")
        # EXCEPTION
        if recv[:3] != "334":
            raise IOError
        recv = self._send_n_recv(base64.b64encode(user.encode()) + b"\r\n")
        # EXCEPTION
        if recv[:3] != "334":
            raise IOError
        recv = self._send_n_recv(base64.b64encode(password.encode()) + b"\r\n")
        return int(recv[:3])

    def quit(self) -> int:
        command = "QUIT"
        recv = self._send_n_recv(command.encode() + b"\r\n")
        self._SSLSocket.close()
        return int(recv[:3])

    def _send_n_recv(self, bytes):
        self._SSLSocket.send(bytes)
        recv = self._SSLSocket.recv(1024)
        return recv.decode()

class SMTPMsg():

    def __init__(self, fromMail, toMail) -> None:
        self._code = f"MIME-Version: 1.0\r\n".encode()
        self._code += f"From: {fromMail}\r\nTo: {toMail}\r\n".encode()
        self.boundary = ""

    def add_type(self, value, boundary=""):
        self._code += f"Content-Type: {value}".encode()
        if boundary:
            self._code += f"; boundary=\"{boundary}\"".encode()
            self.boundary = boundary
        self._code += "\r\n".encode()

    def add_disposition(self, value, filename=""):
        self._code += f"Content-Disposition: {value}".encode()
        if filename:
            self._code += f"; filename=\"{filename}\"".encode()
        self._code += b"\r\n" 

    def add_boundary(self):
        self._code += f"\r\n\r\n--{self.boundary}\r\n".encode()

    def add_end(self):
        self._code += f"\r\n\r\n--{self.boundary}--".encode()

    def add_content_encoding(self, value):
        self.add_header("Content-Transfer-Encoding", value)

    def add_header(self, key, value):
        self._code += f"{key}: {value}\r\n".encode()
    
    def add_data(self, bytes):
        self._code += b"\r\n" + bytes

    def add_crlf(self):
        self._code += b"\r\n"

    def encode(self):
        return self._code





MIMA_TYPES = {"txt" : "text/plain",
              "html": "text/html",
              "mp3" : "audio/mpeg",
              "jpg" : "image/jpeg",
              "png" : "image/png"}