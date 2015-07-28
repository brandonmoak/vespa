import agent_base
import time
from vespa.utilities.util import get_default_parser

from vespa.event.event import RegistrationRequest


class BasicAgent(agent_base.AgentBase):
    def __init__(self, config, args, networkedagents, localagents, events):
        super(BasicAgent, self).__init__(config, networkedagents, localagents, events, args)
        self.events.subscribe_to_event(RegistrationRequest, self.on_register)

    def on_register(self, msg):
        self.logger.info('on registration')

    def tick(self, dt):
        print '-------Networked Agents----------'
        for netagent in self.networkedagents:
            self.logger.info([netagent.config.agentname,
                              netagent.config.address,
                              netagent.config.agentid])
        time.sleep(.5)

parser = get_default_parser()
args = parser.parse_args()

if __name__ == '__main__':
    BasicAgent(agent_base.load_config(args.collection, args.agent), args)
