from agent_base import AgentBase, get_default_parser, load_config
import vespa.event.event as event
import window_agent


class ShapeAgent(AgentBase):
    def __init__(self, config, args):
        super(ShapeAgent, self).__init__(config, args)
        self.handler.subscribe_to_event(window_agent.MouseUpdate, self.on_mouse_update)

    def tick(self, dt):
        pass

    def on_mouse_update(self, msg):
        self.logger.info([msg.timestamp, msg.x, msg.y])
        self.config.x = msg.x
        self.config.y = msg.y
        self.event_all_agents(
            ShapeUpdate(self.config.agentid,
                        'all',
                        self.config.x,
                        self.config.y,
                        self.config.size))

    def move(self, dx, dy):
        self.config.x += dx
        self.config.y += dy


class ShapeUpdate(event.Event):
    def __init__(self, senderid, receiverid, x, y, size):
        super(ShapeUpdate, self).__init__(senderid, receiverid)
        self.x = x
        self.y = y
        self.size = size

parser = get_default_parser()
args = parser.parse_args()

if __name__ == '__main__':
    ShapeAgent(load_config(args.collection, args.agent), args)
