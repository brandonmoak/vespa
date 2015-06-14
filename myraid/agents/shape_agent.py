from agent_base import AgentBase
import myraid.message.message as message
import argparse


class ShapeAgent(AgentBase):
    class Meta:
        def __init__(self):
            self.x = None
            self.y = None
            self.size = None

    def __init__(self, args):
        super(ShapeAgent, self).__init__(args.config, args.commtype, args.host)
        self.meta = ShapeAgent.Meta()
        self.meta.x = 0
        self.meta.y = 0
        self.meta.size = 0

    def tick(self, dt):
        self.resolve_contraints()
        self.message_all_agents(
            self.agentid,
            'all',
            self.meta.x,
            self.meta.y,
            self.meta.size)

    def move(self, dx, dy):
        self.config.x += dx
        self.config.y += dy

    def resolve_contraints(self):
        pass


class SquareAgent(ShapeAgent):
    def __init__(self, args):
        super(SquareAgent, self).__init__(args)


class TriangleAgent(ShapeAgent):
    def __init__(self, args):
        super(TriangleAgent, self).__init__(args)


class CircleAgent(ShapeAgent):
    def __init__(self, args):
        super(CircleAgent, self).__init__(args)


class ShapeUpdate(message.Message):
    def __init__(self, senderid, receiverid, x, y, size):
        super(ShapeUpdate, self).__init__(senderid, receiverid)
        self.x = x
        self.y = y
        self.size = size

parser = argparse.ArgumentParser()
parser.add_argument('--host', help='host agent ip address, used to intialize communications')
parser.add_argument('--config')
parser.add_argument('--commtype')
parser.add_argument('--shape')
args = parser.parse_args()

if __name__ == '__main__':
    if args.shape == 'square':
        SquareAgent(args)
    if args.shape == 'triangle':
        TriangleAgent(args)
    if args.shape == 'circle':
        CircleAgent(args)
