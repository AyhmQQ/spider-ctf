
import socket
import time

class NetcatClient:
    def __init__(self, host, port, timeout=5):
        self.host = host
        self.port = port
        self.timeout = timeout

    def receive_passive(self, limit=4096):
        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as s:
                data = s.recv(limit)
                return data.decode('utf-8', errors='ignore')
        except Exception as e:
            return f"Error connecting to {self.host}:{self.port} - {e}"
