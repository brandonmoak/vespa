import threading
import time
import argparse
import copy

from vespa.message.messagehandler import MessageHandler, message_handler
import vespa.message.message as message
from vespa.utilities.helpers import generate_random_string
import vespa.config
from vespa.comm import udpcomm


class AgentBase(object):
    """
    Base class for each agent, handles all communication between agents
    """
    def __init__(self, args):
        self.alive = True
        self.networkedagents = []
        commtype, host_group = args.commtype, args.host_group

        self.handler = MessageHandler()
        self.handler.subscribe_to_message_type(message.Registration,
                                               self.add_networked_agent)
        self.handler.subscribe_to_message_type(message.Shutdown, self.kill)

        self.config = load_config(host_group, args.agent)
        self.config.hostaddr = get_host_adress(host_group)
        self.config.agentid = generate_random_string()
        self.config.name = args.agent
        self.config.host_group = host_group
        self.config.commtype = commtype

        self.comm = load_commtype(commtype, self.config)

        self._spawn_threads()
        self.register_with_host()

    # ################### Functions to be overwritten #########################
    # #########################################################################

    def tick(self, dt):
        raise NotImplementedError('tick(self, dt) must be overwritten')

    # ########################## Public functions #############################
    # #########################################################################

    def register_with_host(self):
        self.enqueue_message(
            message.Registration(
                self.config.host_group,
                self.config.name,
                type(self),
                self.config.agentid,
                self.config.address
            ), self.config.hostaddr)

    def enqueue_message(self, message, destination):
        msg = message.flatten()
        self.comm.write(msg, destination)

    def message_all_agents(self, msg):
        for netagent in self.networkedagents:
            netagent.send_message_to(msg.flatten())

    def kill(self):
        self.comm.shutdown()
        self.alive = False

    def heartbeat(self):
        print 'heart'

    # ########################### Message Handlers ############################
    # #########################################################################

    @message_handler(message.Registration)
    def add_networked_agent(self, msg):
        agent = filter(
            lambda x: x.config.agentid == msg.senderid, self.networkedagents)
        if len(agent) == 0:
            # pass on new node to the rest of the network
            self.message_all_agents(msg)

            # add store list of agents on network
            newagent = NetworkedAgent(
                self.comm,
                msg.host_group,
                msg.name,
                msg.type,
                msg.senderid,
                msg.senderaddr)
            self.networkedagents.append(newagent)

            # respond to registration
            newagent.send_message_to(
                message.Registration(
                    self.config.host_group,
                    self.config.name,
                    type(self),
                    self.config.agentid,
                    self.config.address
                    ).flatten()
                )
        else:
            # Agent already in network
            pass

    # ########################### Private functions ###########################
    # #########################################################################

    def _spawn_threads(self):
        self.ticker = threading.Thread(target=self._tick)
        self.ticker.start()

    def _tick(self):
        """
        fires on a regular basis, tasks will be processed here
        """
        last = time.time()
        while self.alive:
            self._check_inbox()
            now = time.time()
            dt = now - last
            self.tick(dt)
            last = time.time()
            time.sleep(.01)

    def _check_inbox(self):
        msg = self.comm.read()
        if msg is not None:
            self.handler.handle_message(msg)

# ###########################  Networked Agent  ###########################
# #########################################################################


class NetworkedAgent(object):
    """
    agents that have been registered onto an agents network,
    simulates its attributes
    """
    def __init__(self, comm, host_group, agentname, agenttype, agentid, addr):
        self.config = load_config(host_group, agentname)
        self.comm = comm
        self.config.agentname = agentname
        self.config.agentid = agentid
        self.config.address = addr
        self.config.host_group = host_group

    def send_message_to(self, message):
        self.comm.write(message, self.config.address)

    def add_attribute(self, attribute, value):
        setattr(self, attribute, value)

# ##############################  Utilities  ##############################
# #########################################################################


def load_commtype(commtype, agentconfig):
    if commtype == 'udp':
        return udpcomm.UDPComm(agentconfig)
    else:
        raise NotImplementedError('commtype has not been defined!')


def load_config(host_group, name):
    package = vespa.config
    prefix = ".".join([package.__name__, host_group])
    config = __import__('.'.join([prefix, name]), fromlist=package.__name__)
    return copy.deepcopy(config.Config)


def get_type_from_config(host_group, agentname):
    pass


def get_host_adress(host_group):
    """
    Gets host address from host group
    If unable to get host address, endure that hostname has
    been defined in the __init__ of the host_group.
    see .config.host_group.__init__ for example
    """
    package = vespa.config
    module = '.'.join([package.__name__, host_group])
    module = __import__(module, fromlist=package.__name__)
    if module.host is not None:
        return module.host.Config.address


def get_default_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--host_group',
                        help='group that agent is a member of')
    parser.add_argument('--agent',
                        help='name of agent that is to be launched')
    parser.add_argument('--commtype',
                        help='type of communication that agents use')
    return parser
