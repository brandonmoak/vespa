from collections import deque
import time
import threading


class Comm(object):
    """
    Base class for communcaiton interfaces, examples of overwritten
    class is udpcomm and tcpcomm. template to come...
    """
    def __init__(self, maxbufferlen=256):
        self.alive = True
        self.setup()
        self.inbound = deque(maxlen=256)
        self.outbound = deque(maxlen=256)
        self._spawn_threads()

    # ################### Functions to be overwritten #########################
    # #########################################################################

    def send(self, message, address):
        "Method for child class to send messages"
        raise NotImplementedError()

    def setup(self):
        """
        sets up the watch thread in the child class if necessary
        """
        pass

    def watcher(self):
        """
        watches the port that the inbound messages will be coming,
        must be defined by child class
        """
        raise NotImplementedError('port watcher must be defined')

    # ########################## Public functions #############################
    # #########################################################################

    def write(self, message, address):
        "Not to be overwritten by child class"
        self.outbound.append((message, address))

    def shutdown(self):
        self.alive = False

    def read(self):
        if len(self.inbound) > 0:
            return self.inbound.popleft()
        else:
            return None

    # ########################### Private functions ###########################
    # #########################################################################

    def _spawn_threads(self):
        self._read = threading.Thread(target=self._reader)
        self._write = threading.Thread(target=self._writer)
        self._read.start()
        self._write.start()

    def _reader(self):
        while self.alive:
            time.sleep(.001)
            self.watcher()

    def _writer(self):
        while self.alive:
            if len(self.outbound) > 0:
                msg, address = self.outbound.popleft()
                self.send(msg, address)


class OutboundWatch:
    """
    Ensures that message sent have been responded to,
    if not messages are resent after a configured time
    """
    pass
