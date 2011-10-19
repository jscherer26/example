import logging
import logging.handlers

import collections

class BufferedHandler(logging.Handler):

    def __init__(self, capacity, flushLevel, target):

        logging.Handler.__init__(self)
        self.records = collections.deque(maxlen = capacity)
        self.capacity = capacity
        self.flushLevel = flushLevel
        self.target = target
        self.index = 0

    def flush(self):

        print 'flush() ... Target >>%s<<' % (self.target)
        self.target.flush()

    def emit(self, record):

        if record.levelno >= self.flushLevel:
            # flush all stored items
            for rec in self.records:
                self.target.emit(rec)
            self.records.clear()
            self.target.emit(record)
        else:
            # add message to history queue
            self.records.append(record)
