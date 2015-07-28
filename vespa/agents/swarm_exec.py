import agent_base
import shape_agent
from vespa.utilities.util import get_default_parser

parser = get_default_parser()
args = parser.parse_args()


class SwarmExecutive(agent_base.AgentBase):
    def __init__(self, config, networkedagents, localagents, events, args):
        super(SwarmExecutive, self).__init__(config, networkedagents, localagents, events, args)
        self.events.subscribe_to_event(shape_agent.ShapeUpdate, self.on_shape_update)

    def tick(self, dt):
        """
        called on a regular basis, this is the main loop for each agent
        to process its own tasks
        """
        self.sleep(.5)
        f = self.first_agent_with(agentname='first')
        if f is not None:
            print f.config.x, f.config.y
        positions = self.config.position_template(['first', 'centroid'])
        positions['first']['pos'] = [-3, -4]
        positions['centroid']['pos'] = [0, 0]
        print self.config.resolve(positions)

    def on_shape_update(self, msg):
        age = self.first_agent_with(agentid=msg.senderid)
        age.config.x, age.config.y = msg.x, msg.y

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
