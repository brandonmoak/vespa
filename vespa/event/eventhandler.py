import threading
import time
from vespa.utilities.helpers import Enum, generate_random_string
from collections import deque

HandlerStatus = Enum(['initialized', 'processing', 'error', 'stopped'])


class EventHandler:
    """
    to subscribe to events from other agents the event_type
    must be connected to the user defined function in the event handler
    """
    def __init__(self, inbox):
        self.inbox = inbox
        self.lookup = {}
        self.workers = []
        self.unprocessed = deque(maxlen=200)
        self.alive = True
        self._inbox = threading.Thread(target=self._monitor_inbox)
        self._watcher = threading.Thread(target=self._watch)
        self._inbox.start()
        self._watcher.start()

    def _monitor_inbox(self):
        while self.alive:
            if len(self.inbox) > 0:
                e = self.inbox.popleft()
                self.handle_event(e)

    def _watch(self):
        """
        watches the event handlers
        """
        while self.alive:
            _new = filter(lambda x:
                          x['_status'] == HandlerStatus.initialized,
                          self.workers)
            for worker in _new:
                try:
                    worker['_worker'].start()
                    worker['_status'] = HandlerStatus.processing
                    worker['_starttime'] = time.time()
                except Exception, e:
                    print e

            _stopped = filter(lambda x:
                              (x['_status'] == HandlerStatus.stopped or
                               x['_status'] == HandlerStatus.error),
                              self.workers)

            for worker in _stopped:
                try:
                    # print 'deleting', worker
                    del self.workers[self.workers.index(worker)]
                except Exception, e:
                    print e

    def handle_event(self, event):
        if event.event_type in self.lookup:
            wid = generate_random_string()
            for handler in self.lookup[event.event_type]:
                self.workers.append(
                    {'_worker': threading.Thread(
                                    target=self.processor,
                                    args=(handler, event, wid)),
                     '_status': HandlerStatus.initialized,
                     '_workerid': wid}
                    )
        else:
            #print 'unprocessed', event.__dict__
            self.unprocessed.append(event)

    def subscribe_to_event(self, eventtype, function):
        if eventtype.__name__ not in self.lookup:
            self.lookup[eventtype.__name__] = []
        self.lookup[eventtype.__name__].append(function)

    def processor(self, handler, event, workerid):
        '''
        events handlers will be processed here, ran in its own thread
        '''
        try:
            handler(event)
        except Exception, e:
            event = 'Error in handler - {0}: {1}'.format(handler.__name__, e)
            print event
            worker = filter(
                lambda x: x['_workerid'] == workerid, self.workers)[0]
            worker['_status'] = HandlerStatus.error

    def shutdown(self):
        self.alive = False






# runs independently of agents
# agents can subscribe to message type, sender_agent_type, 
# agents can fire event
# message can be sent to specific agent?

# event.fire(event.update)