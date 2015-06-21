import threading
import time
import argparse
import copy

import vespa.event.message as message
import vespa.config
from vespa.event.messagehandler import MessageHandler
from vespa.utilities.helpers import generate_random_string
from vespa.utilities.log import LoggingMixIn
from vespa.comm import udpcomm


class AgentBase(LoggingMixIn):
    """
    Base class for each agent, handles all communication between agents
    """
    def __init__(self, config, args):
        super(AgentBase, self).__init__(args)
        self.alive = True
        self.networkedagents = []
        commtype, collection = args.commtype, args.collection
        self.handler = MessageHandler()
        self.handler.subscribe_to_message(message.Registration,
                                          self.add_networked_agent)
        self.config = config
        self.config.hostaddr = get_host_adress(collection)
        self.config.agentid = generate_random_string()
        self.config.name = args.agent
        self.config.collection = collection
        self.config.commtype = commtype

        self.comm = load_commtype(commtype, self.config)

        self.timer(1, self._spawn_threads)
        self.timer(2, self.register_with_exec)

        self.logger.info('[AGENT] ' + ', '.join([self.config.name,
                                                self.config.collection,
                                                self.config.agentid,
                                                str(self.config.address)]))

    # ################### Functions to be overwritten #########################
    # #########################################################################

    def tick(self, dt):
        raise NotImplementedError('tick(self, dt) must be overwritten')

    # ########################## Public functions #############################
    # #########################################################################

    def register_with_exec(self):
        self.enqueue_message(
            message.Registration(
                self.config.collection,
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

    def timer(self, timeout, function, *args, **kwargs):
        t = threading.Timer(timeout, function, *args, **kwargs)
        t.start()

    # ########################### Message Handlers ############################
    # #########################################################################

    def add_networked_agent(self, msg):
        agent = filter(
            lambda x: x.config.agentid == msg.senderid, self.networkedagents)
        if len(agent) == 0 and msg.senderid != self.config.agentid:
            self.logger.info(
                'Recieved registration request from: {0}'.format(msg.name))
            # pass on new node to the rest of the network
            self.message_all_agents(msg)

            # add store list of agents on network
            newagent = NetworkedAgent(
                self.comm,
                msg.collection,
                msg.name,
                msg.type,
                msg.senderid,
                msg.senderaddr)
            self.networkedagents.append(newagent)

            # respond to registration
            newagent.send_message_to(
                message.Registration(
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

    # ########################### Private functions ###########################
    # #########################################################################

    def _spawn_threads(self):
        self._inbox = threading.Thread(target=self._check_inbox)
        self.ticker = threading.Thread(target=self._tick)
        self.ticker.start()
        self._inbox.start()

    def _tick(self):
        """
        fires on a regular basis, calls main loop in child class
        """
        last = time.time()
        while self.alive:
            try:
                now = time.time()
                dt = now - last
                self.tick(dt)
                last = time.time()
            except Exception, e:
                print e

    def _check_inbox(self):
        while self.alive:
            msg = self.comm.read()
            if msg is not None:
                self.handler.handle_message(msg)
            time.sleep(.01)

# ###########################  Networked Agent  ###########################
# #########################################################################


class NetworkedAgent(object):
    """
    agents that have been registered onto an agents network,
    simulates its attributes
    """
    def __init__(self, comm, collection, agentname, agenttype, agentid, addr):
        self.config = load_config(collection, agentname)
        self.comm = comm
        self.config.agentname = agentname
        self.config.agentid = agentid
        self.config.address = addr
        self.config.collection = collection

    def send_message_to(self, message):
        self.comm.write(message, self.config.address)

    def add_attribute(self, attribute, value):
        setattr(self, attribute, value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{0}'.format(', '.join([self.config.agentname,
                                       self.config.agentid,
                                       str(self.config.address),
                                       self.config.collection]))

# ##############################  Utilities  ##############################
# #########################################################################


def load_commtype(commtype, agentconfig):
    if commtype == 'udp':
        return udpcomm.UDPComm(agentconfig)
    else:
        raise NotImplementedError('commtype has not been defined!')


def load_config(collection, name):
    """
    loads config.collecion.name
    """
    package = vespa.config
    prefix = ".".join([package.__name__, collection])
    config = __import__('.'.join([prefix, name]), fromlist=package.__name__)
    config.Config.verify_override()
    return copy.deepcopy(config.Config)


def get_type_from_config(collection, agentname):
    pass


def get_host_adress(collection):
    """
    Gets host address from host group
    If unable to get host address, endure that hostname has
    been defined in the __init__ of the collection.
    see .config.collection.__init__ for example
    """
    package = vespa.config
    module = '.'.join([package.__name__, collection])
    module = __import__(module, fromlist=package.__name__)
    if module.host is not None:
        return module.host.Config.address


def get_default_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--collection',
                        help='group that agent is a member of')
    parser.add_argument('--agent',
                        help='name of agent that is to be launched')
    parser.add_argument('--commtype',
                        help='type of communication that agents use')
    parser.add_argument('--log_level',
                        help='severity of logging to print')
    return parser
