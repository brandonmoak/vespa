from vespa.event.event import TransAction, Event


class NetworkedAgent(object):
    """
    agents that have been registered onto an actors network
    """
    def __init__(self, link, identifier):
        self.link = link
        self.identifier = identifier
        self.status = 'initialized'

    def add_event_to_inbox(self, event):
        data = event.flatten()

        transaction = Event(event.senderid,
                            TransAction,
                            target=self.identifier.agentid,
                            event=data,
                            interface='default')

        self.link.write(transaction.flatten(), self.identifier.address)

    def add_attribute(self, attribute, value):
        setattr(self, attribute, value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{0}'.format(', '.join([self.agentname,
                                       self.agentid,
                                       str(self.address),
                                       self.collection]))


class AgentIdentifier(object):
    def __init__(self, agenttype, agentname, agentid, interface, address, actor):
        self.agenttype = agenttype
        self.agentname = agentname
        self.agentid = agentid
        self.interface = interface
        self.actor = actor
