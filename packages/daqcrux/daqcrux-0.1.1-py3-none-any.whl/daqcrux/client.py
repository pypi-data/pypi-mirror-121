import socket
import json

class client:
    """! Clase para comunicación vía sockets. Class definition for sockets communication
    """
    def __init__(self, host, port):
        """! Class constructor
        @param host Hostname.
        @param port Socket's port.
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        """! Function to perform the socket connection
        """
        self.sock.connect((self.host, self.port))

    def sock_send(self, data):
        """! Function to send data trough the socket
        @param data Data in JSON format
        """
        self.sock.sendall(bytes(json.dumps(data), encoding = "utf-8"))

    def sock_recieve(self):
        """! Function to recieve server data
        @return response Server response
        """
        response = self.sock.recv(1024)
        return response