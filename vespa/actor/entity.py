import actor
import vespa.config.entities
from vespa.agents.agent_base import load_config
from vespa.utilities.util import get_default_parser

parser = get_default_parser()
args = parser.parse_args()


class Entity(actor.Actor):
    actor_interface = actor.interfaces.Entity

    def __init__(self, args):
        super(Entity, self).__init__(args)
        self.load_entity_agents(args.actor)

    def load_entity_agents(self, entity):
        """
        loads config.package.name
        """
        module_config = vespa.config.entities
        prefix = ".".join([module_config.__name__])
        e = __import__('.'.join([prefix, entity]), fromlist=module_config.__name__)
        a = filter(lambda x: '__' not in x, e.__all__)
        for agent in a:
            self.launch_agent(load_config('.'.join(['entities', entity]), agent))


    def swarm(self):
        pass

    def release_swarm(self):
        pass

    def register_with_executive(self):
        pass

    
if __name__ == '__main__':
    Entity(args)