from comm import Comm
import socket


class UDPComm(Comm):
    def __init__(self, config):
        self.config = config
        super(UDPComm, self).__init__(config)

    def setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.config.address)

    def watcher(self):
        self.sock.settimeout(.1)
        try:
            data, addr = self.sock.recvfrom(1024)
            self.inbound.append(data)
        except socket.timeout:
            pass

    def send(self, message, destination):
        self.sock.sendto(message, destination)

    def shutdown(self):
        super(UDPComm, self).shutdown()
        self.sock.close()
