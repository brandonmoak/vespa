import agent_base
import time

from vespa.message.message import Registration


class BasicAgent(agent_base.AgentBase):
    def __init__(self, config, args):
        super(BasicAgent, self).__init__(config, args)
        self.handler.subscribe_to_message(Registration, self.on_register)

    def on_register(self, msg):
        self.logger.info('on registration')

    def tick(self, dt):
        print '-------Networked Agents----------'
        for netagent in self.networkedagents:
            self.logger.info([netagent.config.agentname,
                              netagent.config.address,
                              netagent.config.agentid])
        time.sleep(.5)

parser = agent_base.get_default_parser()
args = parser.parse_args()

if __name__ == '__main__':
    BasicAgent(agent_base.load_config(args.agent), args)
