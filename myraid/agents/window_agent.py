import time
from myraid.message.message.message import Registration
from agent_base import AgentBase, get_default_parser, load_config
from shape_agent import ShapeUpdate
import myraid.plotting.window as window


class WindowAgent(AgentBase):
    def __init__(self, config, args):
        super(WindowAgent, self).__init__(config, args)
        self.handler.subscribe_to_message(Registration, self.create_new_shape)
        self.handler.subscribe_to_message(ShapeUpdate, self.position_update)
        self.win = window.Window(
            self.config.win_name,
            self.config.win_x,
            self.config.win_y)

    def tick(self, dt):
        time.sleep(1)

    def create_new_shape(self, msg):
        # find out who the message came from
        agent = next((i for i in self.networkedagents if
                      i.agentid == msg.senderid), None)
        if agent is None:
            # Initialize on window
            self.win.add_circle(msg.senderid, x=0, y=0, rad=10)

    def position_update(self, msg):
        # find out who the message came from
        agent = next((i for i in self.networkedagents if
                      i.agentid == msg.senderid), None)
        if agent is not None:
            agent.config.x = msg.x
            agent.config.y = msg.y
            agent.config.size = msg.size
            p = '{2}| x: {0} y: {1}'.format(agent.config.x,
                                            agent.config.y,
                                            agent.config.name)
            self.logger.info(p)

            self.win.set_shape_pos(msg.senderid,
                                   self.confi.x,
                                   self.config.y)

parser = get_default_parser()
args = parser.parse_args()

if __name__ == '__main__':
    WindowAgent(load_config(args.agent), args)
