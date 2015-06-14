import agent_base
import time


class BasicAgent(agent_base.AgentBase):
    def __init__(self, args):
        super(BasicAgent, self).__init__(args)

    def tick(self, dt):
        print '-------Networked Agents----------'
        for netagent in self.networkedagents:
            self.logger.info([netagent.config.agentname, netagent.config.address, netagent.config.agentid])
        time.sleep(.5)

parser = agent_base.get_default_parser()
args = parser.parse_args()

if __name__ == '__main__':
    BasicAgent(args)
