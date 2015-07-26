from event import BroadcastLevel


class Pipeline:
    """
    For messaging a wide audience of agents
    """
    def __init__(self, local_agents, networkedagents):
        self.local_agents = local_agents
        self.networkedagents = networkedagents

    def forward(self, event, interface='default', level=BroadcastLevel.local):
        # TODO add interface filter
        print 'forwarding event: ', event.target, event
        if level == BroadcastLevel.local:
            for agent in self.local_agents:
                agent.add_event_to_inbox(event)
        elif level == BroadcastLevel.all:
            for agent in self.local_agents + self.networkedagents:
                agent.add_event_to_inbox(event)
        else:
            try:
                filter(lambda x: x.agentid == event.target,
                       self.local_agents + self.networkedagents).add_event_to_inbox(event)
            except:
                print 'Unable to forward event: ', event
