import agent_base
from vespa.utilities.util import get_default_parser
from vespa.link.udp_link import UDPLink
import vespa.event.event as event
import threading
from networked_agent import NetworkedAgent, AgentIdentifier

parser = get_default_parser()
args = parser.parse_args()


class TransActorAgent(agent_base.AgentBase):
    """
    relays and accepts messages from other actors, defined for only
    udp communcaiton at the moment
    instantiates netwokred agents that come in from other actors
    """
    def __init__(self, config, networkedagents, localagents, events, args):
        super(TransActorAgent, self).__init__(
                                    config, networkedagents, localagents, events, args)
        # subscribe to registration requests #TODO

        self.udplink = UDPLink(self.config.address)
        self.add_event_handler(event.LocalRegistrationRequest, self.on_registration_request)
        self.add_event_handler(event.IdentifierExchange, self.parse_identifier)
        self.add_event_handler(event.TransAction, self.on_transaction)

        self._spawn_watchers()

        # self.timer(2, self._connect_with_exec)

    def tick(self, dt):
        """
        called on a regular basis, this is the main loop for each agent
        to process its own tasks
        """
        # print 'to be implemented'
        pass

    # IDENTIFIER FUNCTIONS
    def create_identifier_from_local_agent(self, agent):
        return AgentIdentifier(self,
                               agent.config.agenttype,
                               agent.config.agentname,
                               agent.config.agentid,
                               None,
                               agent.config.actor)

    def get_local_identifier_list(self):
        identifierlist = []
        for agent in self.localagents:
            identifierlist.append(self.create_identifier_from_agent(agent))
        return identifierlist

    def create_identifier_from_net_agent(self, agent):
        return AgentIdentifier(self,
                               agent.identifier.agenttype,
                               agent.identifier.identifier.agentname,
                               agent.identifier.agentid,
                               None,
                               agent.identifier.actor)

    def get_net_identifier_list(self):
        identifierlist = []
        for agent in self.networkedagents:
            identifierlist.append(self.create_identifier_from_agent(agent))
        return identifierlist

    def parse_identifier(self, e):
        print e.data['address'], e.data['identifiers']

        new = set(e.data['identifiers']).difference(set(self.get_net_identifier_list()))
        dif = set(self.get_net_identifier_list() + self.get_local_identifier_list())\
            .difference(set(e.data['identifiers']))

        for ident in list(new):
            self.networkedagents.append(self.create_networked_agent(ident))

        # Respond to identifier exchange
        self.udplink.send(event.Event(type=event.IdentifierExchange,
                                      identifiers=list(dif),
                                      actor=self.actor,
                                      address=self.udplink.address).flatten(),
                          e.data['address'])

        self.logger.debug(self.networkedagents)

    def create_networked_agent(self, identifier):
        return NetworkedAgent(self.udplink, identifier)

    # ON TRANSACTION
    def on_transaction(self, e):
        pass

    # REGISTRATION REQUEST
    def on_registration_request(self, event):
        # registration event from other agents
        print 'ON REGISTRATION REQUEST CALLED'
        print event
        self.respond_to_registration(event.senderid)

    def respond_to_registration(self, agentid):
        e = event.Event(self.config.agentid,
                        event.LocalRegistrationConfirmed,
                        name=self.config.name,
                        actor=self.config.actor,
                        interfaces=None)
        self.first_agent_with(self.localagents, agentid=agentid).add_event_to_inbox(e)

    # PRIVATE FUNCTIONS
    def _connect_with_exec(self, address):
        self.udplink.send(event.Event(type=event.IdentifierExchange,

                                      identifiers=self.get_local_identifier_list(),
                                      address=self.udplink.address).flatten(),
                          self.config.address)

    def _spawn_watchers(self):
        self._inbound = threading.Thread(target=self._check_inbound)
        self._inbound.start()

    def _check_inbound(self):
        # process messages that have come in the inbox, fire to
        # target actors
        # inbound messages are of type IdentifierExchange or TransAction
        while self.alive:
            e = self.udplink.read()
            if e is not None:
                try:
                    self.add_event_to_inbox(event.Event.unflatten(e))
                except:
                    print 'unable to unflatten event', e
