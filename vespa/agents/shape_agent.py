from agent_base import AgentBase, get_default_parser
import vespa.message.message as message
import window_agent


class ShapeAgent(AgentBase):
    def __init__(self, config, args):
        super(ShapeAgent, self).__init__(config, args)
        self.handler.subscribe_to_message(window_agent.MouseUpdate, self.on_mouse_update)

    def tick(self, dt):
        self.resolve_contraints()
        self.message_all_agents(
            ShapeUpdate(self.config.agentid,
                        'all',
                        self.config.x,
                        self.config.y,
                        self.config.size))

    def on_mouse_update(self, msg):
        self.logger.debug([msg.messageid, msg.senderid, msg.x, msg.y])

    def move(self, dx, dy):
        self.config.x += dx
        self.config.y += dy

    def resolve_contraints(self):
        pass


class ShapeUpdate(message.Message):
    def __init__(self, senderid, receiverid, x, y, size):
        super(ShapeUpdate, self).__init__(senderid, receiverid)
        self.x = x
        self.y = y
        self.size = size

parser = get_default_parser()
args = parser.parse_args()

if __name__ == '__main__':
    ShapeAgent(load_config(args.agent), args)
