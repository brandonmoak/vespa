import threading
import time
from message import Message
from vespa.utilities.helpers import Enum, generate_random_string

HandlerStatus = Enum(['default', 'initialized', 'processing', 'error', 'stopped'])


class MessageHandler:
    """
    to subscribe to messages from other agents the message_type must be connected to the
    user defined function in the message handler
    """
    def __init__(self):
        self.lookup = {}
        self.workers = []
        self.unprocessed = []
        self.alive = True
        self._watcher = threading.Thread(target=self._watch)
        self._watcher.start()

    def _watch(self):
        """
        watches the message handlers
        """
        while self.alive:
            _new = filter(lambda x: x['_status'] == HandlerStatus.initialized, self.workers)
            for worker in _new:
                try:
                    worker['_worker'].start()
                    worker['_status'] = HandlerStatus.processing
                    worker['_starttime'] = time.time()
                except Exception, e:
                    print e

            _stopped = filter(lambda x: (x['_status'] == HandlerStatus.stopped or
                                         x['_status'] == HandlerStatus.error),
                              self.workers)

            for worker in _stopped:
                try:
                    print 'deleting', worker
                    del self.workers[self.workers.index(worker)]
                except Exception, e:
                    print e

    def subscribe_to_message_type(self, message_type, function):
        if message_type.__name__ not in self.lookup:
            self.lookup[message_type.__name__] = function

    def unsubscribe_to_message_type(self, message_type):
        if str(message_type) in self.lookup:
            del self.lookup[message_type]

    def handle_message(self, msg):
        message = Message.unflatten(msg)
        if message.message_type in self.lookup:
            wid = generate_random_string()
            self.workers.append(
                {'_worker': threading.Thread(target=self.processor, args=(self.lookup[message.message_type], message, wid, )),
                 '_status': HandlerStatus.initialized,
                 '_workerid': wid}
                )
        else:
            print 'unprocessed', message.__dict__
            self.unprocessed.append(message)

    def processor(self, handler, message, workerid):
        '''
        messages handlers will be processed here, ran in a separate thread
        '''
        try:
            handler(message)
        except Exception, e:
            print e
            worker = filter(lambda x: x['_workerid'] == workerid, self.workers)[0]
            worker['_status'] = HandlerStatus.error

    def shutdown(self):
        self.alive = False


class InvalidMessageType(Exception):
    pass


def message_handler(MessageType):
    def _decorator(f):
        def _function(*args, **kwargs):
            if str(args[1]) == MessageType.__name__:
                return f(*args, **kwargs)
            else:
                raise InvalidMessageType("Message handler recieved an improper message type " + MessageType.__name__)
        return _function
    return _decorator
