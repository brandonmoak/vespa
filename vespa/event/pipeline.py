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
        if level == BroadcastLevel.local:
            print self.local_agents
            for agent in self.local_agents:
                agent.add_event_to_inbox(event)
        elif level == BroadcastLevel.all:
            for agent in self.local_agents + self.networkedagents:
                agent.add_event_to_inbox(event)
        else:
            print 'pipeline.py: Unknown BroadcastLevel'
