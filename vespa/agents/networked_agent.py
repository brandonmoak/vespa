import vespa.event.event as Event

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
        base_message = event.flatten()
        transaction = Event.TransAction
        self.link.write(event, self.config.address)

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
    agent_type
    agent_name
    agent_id
    interface
    parent_actor
