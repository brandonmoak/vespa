from vespa.event.event import RegistrationRequest, Event
from agent_base import AgentBase, load_config
import shape_agent
import vespa.drivers.window as window
from vespa.utilities.util import get_default_parser


class WindowAgent(AgentBase):
    def __init__(self, config, args, networkedagents, localagents, events):
        super(WindowAgent, self).__init__(config, args, networkedagents, localagents, events)
        self.win = window.Window(
            self.config.win_name,
            self.config.win_x,
            self.config.win_y)
        self.events.subscribe_to_event(RegistrationRequest, self.create_new_shape)
        self.events.subscribe_to_event(shape_agent.ShapeUpdate, self.position_update)

    def tick(self, dt):
        pos = self.win.get_last_mouse_pos()
        if pos is not None:
            if (self.config.mouse_x, self.config.mouse_y) != pos:
                self.logger.info(pos)
                self.config.mouse_x, self.config.mouse_y = pos[0], pos[1]
                self.event_all_agents(
                    MouseUpdate(self.config.agentid,
                                'all',
                                self.config.mouse_x,
                                self.config.mouse_y))

    def create_new_shape(self, msg):
        # find out who the event came from
        self.logger.info(self.networkedagents)
        agent = next((i for i in self.networkedagents if
                      i.config.agentid == msg.senderid), None)

        if agent is not None:
            # Initialize on window
            self.logger.info('adding: ' + msg.senderid)
            self.win.add_circle(msg.senderid, x=0, y=0, rad=10)

    def position_update(self, msg):
        # find out who the event came from
        agent = next((i for i in self.networkedagents if
                      i.config.agentid == msg.senderid), None)
        if agent is not None:
            if (msg.x, msg.y) != (agent.config.x, agent.config.y):
                agent.config.x = msg.x
                agent.config.y = msg.y
                agent.config.size = msg.size
                p = '{2}| x: {0} y: {1}'.format(agent.config.x,
                                                agent.config.y,
                                                agent.config.name)
                self.logger.info(p)

                self.win.set_shape_pos(msg.senderid,
                                       agent.config.x,
                                       agent.config.y)


class MouseUpdate(Event):
    def __init__(self, senderid, receiverid, x, y):
        super(MouseUpdate, self).__init__(senderid)
        self.x = x
        self.y = y

parser = get_default_parser()
args = parser.parse_args()

if __name__ == '__main__':
    WindowAgent(load_config(args.collection, args.agent), args)
