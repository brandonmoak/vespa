import agent_base
from vespa.utilities.util import get_default_parser
import vespa.event.event as event
import threading
import time

parser = get_default_parser()
args = parser.parse_args()


class TransActorAgent(agent_base.AgentBase):
    """
    relays and accepts messages from other actors, defined for only
    udp communcaiton at the moment
    """
    def __init__(self, config, args, networkedagents, localagents, events, links):
        super(TransActorAgent, self).__init__(
                                    config, args, networkedagents, localagents, events)
        # subscribe to registration requests #TODO
        self.udplink = self.links['udp']

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
                self.linkudp,
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
        # process messages that have come in the inbox, fire to 
        # target actors
        while self.alive:
            e = self.udplink.read()
            if e is not None:
                self.events.handle_event(e)
