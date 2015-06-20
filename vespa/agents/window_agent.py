import argparse
import time

from agent_base import AgentBase
from vespa.message.messagehandler import message_handler
from shape_agent import ShapeUpdate, ShapeAgent


class WindowAgent(AgentBase):
    def __init__(self, args):
        super(WindowAgent, self).__init__(args)
        self.handler.subscribe_to_message_type(ShapeUpdate, self.position_update)

    def tick(self, dt):
        for agent in self.networkedagents:
            try:
                print self.networkedagents.meta
            except:
                time.sleep(1)

    def draw_agents(self):
        pass

    @message_handler(ShapeUpdate)
    def position_update(self, msg):
        agent = next((i for i in self.networkedagents if i.agentid == msg.senderid), None)
        if agent is not None:
            if not hasattr(agent, 'meta'):
                agent.add_attribute('meta', ShapeAgent.Meta())
            agent.meta.x = msg.x
            agent.meta.y = msg.y
            agent.meta.size = msg.size


parser = argparse.ArgumentParser()
parser.add_argument('--host', help='host agent ip address, used to intialize communications')
parser.add_argument('--config')
parser.add_argument('--commtype')
args = parser.parse_args()

if __name__ == '__main__':
    WindowAgent(args)
