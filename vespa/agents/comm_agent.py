import agent_base
from vespa.utilities.util import get_default_parser
import vespa.event.event as event
from collections import deque
import socket
import threading
import time

parser = get_default_parser()
args = parser.parse_args()


class CommAgent(agent_base.AgentBase):
    """
    relays and accepts messages from other actors
    """
    def __init__(self, config, args, networkedagents, localagents, events):
        super(CommAgent, self).__init__(config, args, networkedagents, localagents, events)
        # subscribe to registration requests
        self.comm = UDPComm(self.config)

    def spawn_threads(self):
        self._inbox = threading.Thread(target=self._check_inbox)
        self._inbox.start()

    def tick(self, dt):
        """
        called on a regular basis, this is the main loop for each agent
        to process its own tasks
        """
        # print 'to be implemented'

    def add_networked_agent(self, e):
        agent = filter(
            lambda x: x.config.agentid == e.senderid, self.networkedagents)
        if len(agent) == 0 and e.senderid != self.config.agentid:
            self.logger.info(
                'Recieved registration request from: {0}'.format(e.name))
            # pass on new node to the rest of the network
            self.event_all_agents(e)

            # add store list of agents on network
            newagent = NetworkedAgent(
                self.comm,
                e.collection,
                e.name,
                e.type,
                e.senderid,
                e.senderaddr)
            self.networkedagents.append(newagent)

            # respond to registration
            newagent.send_event_to(
                event.RegistrationRequest(
                    self.config.collection,
                    self.config.name,
                    type(self),
                    self.config.agentid,
                    self.config.address
                    ).flatten()
                )
        else:
            # Agent already in network
            pass
        self.logger.debug(self.networkedagents)

    def on_network_registration_request(self, event):
        print event

    def on_local_registration_request(self, event):
        print event

    def relay_messages(self):
        pass

    def _check_inbox(self):
        while self.alive:
            e = self.comm.read()
            if e is not None:
                self.events.handle_event(e)
            time.sleep(.01)



class NetworkedAgent(object):
    """
    agents that have been registered onto an actors network
    """
    def __init__(self, comm, collection, agentname, agenttype, agentid, actor):
        self.config = {}
        self.comm = comm
        self.config.agentname = agentname
        self.config.agenttype = agenttype
        self.config.agentid = agentid
        self.config.address = address
        self.config.collection = collection

    def send_event_to(self, event):
        self.comm.write(event, self.config.address)

    def add_attribute(self, attribute, value):
        setattr(self, attribute, value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{0}'.format(', '.join([self.config.agentname,
                                       self.config.agentid,
                                       str(self.config.address),
                                       self.config.collection]))



class Comm(object):
    """
    Base class for communcaiton interfaces, examples of overwritten
    class is udpcomm and tcpcomm. template to come...
    """
    def __init__(self, maxbufferlen=256):
        self.alive = True
        self.connected = False
        self.inbound = deque(maxlen=256)
        self.outbound = deque(maxlen=256)
        self._spawn_threads()
        self.launch_setup()

    # ################### Functions to be overwritten #########################
    # #########################################################################

    def send(self, message, address):
        "Method for child class to send messages"
        raise NotImplementedError()

    def launch_setup(self):
        """
        this function should be called when the connection
        goes down
        """
        self._setup = threading.Thread(target=self.setup())

    def setup(self):
        """
        sets up the watch thread in the child class if necessary, ensures that
        a connection has been made
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
            if self.connected:
                try:
                    time.sleep(.001)
                    self.watcher()
                except:
                    self.connected = False
                    self.launch_setup()

    def _writer(self):
        while self.alive:
            if self.connected:
                try:
                    if len(self.outbound) > 0:
                        msg, address = self.outbound.popleft()
                        self.send(msg, address)
                except:
                    self.connected = False
                    self.launch_setup()


class OutboundWatch:
    """
    Ensures that message sent have been responded to,
    if not messages are resent after a configured time
    """
    pass


class UDPComm(Comm):
    def __init__(self, config):
        self.config = config
        super(UDPComm, self).__init__()

    def setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.config.address)

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
        super(UDPComm, self).shutdown()
        self.sock.close()
