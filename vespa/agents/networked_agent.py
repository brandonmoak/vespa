from vespa.event.event import TransAction, Event


class NetworkedAgent(object):
    """
    agents that have been registered onto an actors network
    """
    def __init__(self, link, address, identifier):
        self.link = link
        self.identifier = identifier
        self.address = address
        self.status = 'initialized'

    def add_event_to_inbox(self, event):
        data = event.flatten()

        transaction = Event(event.senderid,
                            TransAction,
                            target=self.identifier.agentid,
                            event=data,
                            interface='default')

        self.link.write(transaction.flatten(), self.address)

    def add_attribute(self, attribute, value):
        setattr(self, attribute, value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{0}'.format(', '.join([self.config.agentname,
                                       self.config.agentid,
                                       str(self.config.address),
                                       self.config.collection]))


class AgentIdentifier(object):
    def __init__(self, agenttype, agentname, agentid, interface, actor):
        self.agenttype = agenttype
        self.agentname = agentname
        self.agentid = agentid
        self.interface = interface
        self.actor = actor
