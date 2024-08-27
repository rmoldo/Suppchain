class SocketEndpoint:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def equals(self, endpoint):
        return endpoint.ip == self.ip and endpoint.port == self.port
