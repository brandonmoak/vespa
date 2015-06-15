import time
from myraid.message.message import Registration, Message
from agent_base import AgentBase, get_default_parser, load_config
import shape_agent
import myraid.plotting.window as window
import copy


class WindowAgent(AgentBase):
    def __init__(self, config, args):
        super(WindowAgent, self).__init__(config, args)
        self.win = window.Window(
            self.config.win_name,
            self.config.win_x,
            self.config.win_y)
        self.handler.subscribe_to_message(Registration, self.create_new_shape)
        self.handler.subscribe_to_message(shape_agent.ShapeUpdate, self.position_update)
        

    def tick(self, dt):
        pos = self.win.get_last_mouse_pos()
        if pos is not None:
            self.config.mouse_x, self.config.mouse_y = pos[0], pos[1]
            self.message_all_agents(
                MouseUpdate(self.config.agentid,
                            'all',
                            self.config.mouse_x,
                            self.config.mouse_y))

    def create_new_shape(self, msg):
        # find out who the message came from
        agent = next((i for i in self.networkedagents if
                      i.config.agentid == msg.senderid), None)
        if agent is None:
            # Initialize on window
            self.win.add_circle(msg.senderid, x=0, y=0, rad=10)

    def position_update(self, msg):
        # find out who the message came from
        agent = next((i for i in self.networkedagents if
                      i.config.agentid == msg.senderid), None)
        if agent is not None:
            agent.config.x = msg.x
            agent.config.y = msg.y
            agent.config.size = msg.size
            p = '{2}| x: {0} y: {1}'.format(agent.config.x,
                                            agent.config.y,
                                            agent.config.name)
            self.logger.debug(p)

            self.win.set_shape_pos(msg.senderid,
                                   agent.config.x,
                                   agent.config.y)

            

class MouseUpdate(Message):
    def __init__(self, senderid, receiverid, x, y):
        super(MouseUpdate, self).__init__(senderid, receiverid)
        self.x = x
        self.y = y

parser = get_default_parser()
args = parser.parse_args()

if __name__ == '__main__':
    WindowAgent(load_config(args.agent), args)
