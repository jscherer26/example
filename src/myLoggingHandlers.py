import logging
import logging.handlers
import collections

class HistoryHandler(logging.handlers.MemoryHandler):
    def __init__(self, capacity, flushLevel, target):
        logging.handlers.MemoryHandler.__init__(self, capacity)
        self.history = collections.deque(maxlen = capacity)
        self.flushLevel = eval('logging.%s' % (flushLevel))
        self.target = target
        self.index = 0

    def shouldFlush(self, record):
        return False

    def flush(self):
        self.history.clear()

    def emit(self, record):
        if record.levelno >= self.flushLevel:
            # flush all stored items
            for i in self.history:
                self.target.handle(i)
            self.history.clear()
            self.target.handle(record)
        else:
            # add message to history queue
            self.history.append(record)

    def close(self):
        self.flush()
        logging.Handler.close(self)


