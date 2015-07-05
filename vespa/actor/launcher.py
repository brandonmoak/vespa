import entity
import executive
from vespa.utilities.util import get_default_parser

parser = get_default_parser()

if __name__ == '__main__':
    args = parser.parse_args()
    if args.actortype == 'entity':
        print 'launching entity'
        entity.Entity(args)
    elif args.actor == 'executive':
        executive.Executive(args)
    else:
        print 'Invalid Actor Type, define --actortype'

