import threading
import time
import copy
from collections import deque

import vespa.event.event as event
import vespa.config

from vespa.event.event import Event
from vespa.event.eventhandler import EventHandler
from vespa.utilities.util import generate_random_string
from vespa.utilities.log import LoggingMixIn


class AgentBase(LoggingMixIn):
    """
    Base class for each agent, handles all communication between agents
    """
    def __init__(self, config, args, networkedagents, localagents, events):
        super(AgentBase, self).__init__(args)
        self.alive = True
        commtype, collection = args.commtype, args.collection

        self.networkedagents = networkedagents
        self.localagents = localagents
        self.events = events
        self.config = config
        self.inbox = deque(maxlen=100)
        self.handler = EventHandler(self.inbox)

        self.config.hostaddr = get_host_adress(collection)
        self.config.agentid = generate_random_string()
        self.config.name = config.name
        self.config.commtype = commtype

        self.timer(1, self._spawn_threads)

        self.logger.info('[AGENT] ' + ', '.join([self.config.name,
                                                self.config.agentid]))

    # ################### Functions to be overwritten #########################
    # #########################################################################

    def tick(self, dt):
        raise NotImplementedError('tick(self, dt) must be overwritten')

    # ########################## Public functions #############################
    # #########################################################################

    def kill(self):
        raise NotImplementedError
        self.alive = False

    def sleep(self, t):
        time.sleep(t)

    def timer(self, timeout, function, *args, **kwargs):
        t = threading.Timer(timeout, function, *args, **kwargs)
        t.start()

    def fire_event(self, event_type, data):
        self.events.forward(Event(self.agentid, event_type, data))

    # ####################### Event Handler Functions #########################
    # #########################################################################

    def add_event_handler(self, eventtype, function):
        self.event.subscribe_to_event(self.agentid, event, function)

    # ########################## Agent functions ##############################
    # #########################################################################

    def filter_networked_agents(self, agentname=None, agentid=None, agenttype=None, address=None):
        return self.filter_agents(self.networkedagents)

    def filter_local_agents(self, agentname=None, agentid=None, agenttype=None, address=None):
        return self.filter_agents(self.localagents)

    def filter_agents(self, agentlist, agentname=None, agentid=None, agenttype=None, address=None):
        params = {'agentname': agentname,
                  'agentid': agentid,
                  'agenttype': agenttype,
                  'address': address}
        fil = self.agentlist
        for k, val in params.iteritems():
            if val is not None:
                fil = filter(lambda x: getattr(x.config, k) == val, fil)
        return fil

    def first_agent_with(self, agentlist, agentname=None, agentid=None, agenttype=None, address=None):
        fil = self.filter_agents(agentlist, agentname, agentid, agenttype, address)
        return fil[0] if len(fil) > 0 else None

    def add_event_to_inbox(self, event):
        self.inbox.append(event)

    # ########################### Private functions ###########################
    # #########################################################################

    def _spawn_threads(self):
        self.ticker = threading.Thread(target=self._tick)
        self.ticker.start()

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


# ##############################  Utilities  ##############################
# #########################################################################

def load_config(package, name):
    """
    loads config.package.name
    """
    module_config = vespa.config
    prefix = ".".join([module_config.__name__, package])
    config = __import__('.'.join([prefix, name]), fromlist=module_config.__name__)
    config.Config.verify_override()
    return copy.deepcopy(config.Config)


def get_type_from_config(collection, agentname):
    pass


def get_host_adress(collection):
    """
    Gets host address from host group
    If unable to get host address, endure that hostname has
    been defined in the __init__ of the collection.
    see .config.collection_template.__init__ for example
    """
    package = vespa.config
    module = '.'.join([package.__name__, collection])
    module = __import__(module, fromlist=package.__name__)
    if module.host is not None:
        return module.host.Config.address
