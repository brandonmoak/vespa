import vespa.agents as agents
import vespa.utilities.util as util
import vespa.event.pipeline as pipe


interfaces = util.Enum(["Entity"])


class Actor(object):
    """
    The main body that contains agents and supervises their funcitons
    """
    def __init__(self, args):
        self.args = args
        self.local_agents = []
        self.net_agents = []
        self.events = pipe.Pipeline(self.local_agents, self.net_agents)
        self.links = []
        self.launch_essential_agents()

    def launch_essential_agents(self):
        # launch transactor, management actors
        pass

    def launch_agent(self, agent_config):
        print 'launching agent', agent_config
        self.local_agents.append(
            agent_config._launcher(agent_config,
                                   self.args,
                                   self.net_agents,
                                   self.local_agents,
                                   self.events)
            )
        print self.local_agents

    def handle_events(self):
        pass

    def print_agents(self):
        pass

    def initialize_local_agents(self):
        pass

    def start_local_agents(self):
        pass

    def shutdown_local_agents(self):
        pass
