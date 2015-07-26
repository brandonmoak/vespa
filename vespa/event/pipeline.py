from event import Target


class Pipeline:
    """
    Pipeline that connects the local_agents, relays events between agents
    """
    def __init__(self, local_agents, networkedagents):
        self.local_agents = local_agents
        self.networkedagents = networkedagents

    def forward(self, event):
        print 'forwarding event: ', event.target, event
        if event.target == Target.local:
            for agent in self.local_agents:
                agent.inbox.append(event)

        elif event.target == Target.all:
            for agent in self.local_agents:
                agent.inbox.append(event)
            for agent in self.networkedagents:
                agent.send_event_to(event)
        else:
            try:
                filter(lambda x: x.agentid == event.target,
                       self.local_agents + self.networkedagents).add_event_to_inbox(event)
            except:
                print 'Unable to forward event: ', event
