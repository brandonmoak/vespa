from base_link import Link
import socket


class UDPLink(Link):
    def __init__(self, address):
        self.address = address
        super(UDPLink, self).__init__()

    def setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)

        while not self.connected:
            try:
                self.sock.settimeout(.1)
                data = self.sock.recv(1024)
                self.inbound.append(data)
                self.connected = True
            except socket.timeout:
                self.connected = True
            except Exception, e:
                print e
                self.connected = False

    def watcher(self):
        try:
            self.sock.settimeout(.1)
            data, addr = self.sock.recvfrom(1024)
            # print 'recieved', len(data)
            self.inbound.append(data)
        except socket.timeout:
            pass

    def send(self, message, destination):
        # print 'sending', len(message)
        self.sock.sendto(message, destination)

    def shutdown(self):
        super(UDPLink, self).shutdown()
        self.sock.close()
