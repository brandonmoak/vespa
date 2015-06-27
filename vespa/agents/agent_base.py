import threading
import time
import argparse
import copy

import vespa.event.event as event
import vespa.config
from vespa.event.eventhandler import EventHandler
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
        self.handler = EventHandler()
        self.handler.subscribe_to_event(event.RegistrationRequest,
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
        self.enqueue_event(
            event.RegistrationRequest(
                self.config.collection,
                self.config.name,
                type(self),
                self.config.agentid,
                self.config.address
            ), self.config.hostaddr)

    def enqueue_event(self, event, destination):
        e = event.flatten()
        self.comm.write(e, destination)

    def event_all_agents(self, e):
        for netagent in self.networkedagents:
            netagent.send_event_to(e.flatten())

    def kill(self):
        self.comm.shutdown()
        self.alive = False

    def sleep(self, t):
        time.sleep(t)

    def timer(self, timeout, function, *args, **kwargs):
        t = threading.Timer(timeout, function, *args, **kwargs)
        t.start()

    # ########################### Event Handlers ############################
    # #########################################################################

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

    def filter_agents(self, agentname=None, agentid=None, agenttype=None, address=None):
        params = {'agentname': agentname,
                  'agentid': agentid,
                  'agenttype': agenttype,
                  'address': address}
        fil = self.networkedagents
        for k, val in params.iteritems():
            if val is not None:
                fil = filter(lambda x: getattr(x.config, k) == val, fil)
        return fil

    def first_agent_with(self, agentname=None, agentid=None, agenttype=None, address=None):
        fil = self.filter_agents(agentname, agentid, agenttype, address)
        return fil[0] if len(fil) > 0 else None

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
            # try:
                now = time.time()
                dt = now - last
                self.tick(dt)
                last = time.time()
            # except Exception, e:
            #     print e

    def _check_inbox(self):
        while self.alive:
            e = self.comm.read()
            if e is not None:
                self.handler.handle_event(e)
            time.sleep(.01)

# ###########################  Networked Agent  ###########################
# #########################################################################


class NetworkedAgent(object):
    """
    agents that have been registered onto an agents network,
    simulates its attributes
    """
    def __init__(self, comm, collection, agentname, agenttype, agentid, address):
        self.config = load_config(collection, agentname)
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
