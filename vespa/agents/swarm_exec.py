import agent_base
# from vespa.event.messagehandler import message_handler

parser = agent_base.get_default_parser()
args = parser.parse_args()


class SwarmExecutive(agent_base.AgentBase):
    def __init__(self, config, args):
        super(SwarmExecutive, self).__init__(config, args)

    def tick(self, dt):
        """
        called on a regular basis, this is the main loop for each agent
        to process its own tasks
        """
        self.sleep(.5)
        p, q = self.config.position_template(), self.config.position_template()
        p['pos'], q['pos'] = [40], [25]
        positions = {'first': p, 'centroid': q}
        self.config.resolve(positions)

    def broadcast_positions(self):
        """
        relays the generated positional data back to the actor
        """
        pass

    def resolve_contraints(self):
        """
        generates locations of actors in the network
        """
        pass

    def set_centroid(self):
        """
        sets the center position of the swarm
        """
        pass

    def watch_agents(self):
        pass

if __name__ == '__main__':
    SwarmExecutive(agent_base.load_config(args.collection, args.agent), args)
