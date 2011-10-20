#!\usr\bin\python

import sys, time
import traceback
import logging.config
import yaml

from src.myLoggingHandlers import HistoryHandler
from PyQt4 import QtGui
from src.progressbar import ProgressBar
from src.db import DbSqlite3
from src.window import TestWindow

class Example(object):

    def __init__(self):

        self.exceptionCount = 0

        self.config = None
        self.logger = None
        self.database = None
        self.app = None
        self.window = None

    def setup(self):

        self.config = yaml.load(open('config/application.yaml', 'r'))
        logging.handlers.HistoryHandler = HistoryHandler
        logging.config.dictConfig(yaml.load(open(self.config['logging']['config'], 'r')))
        self.logger = logging.getLogger('root')
        self.logger.info('setup()')
        self.database = DbSqlite3(self.config['db']['database'])
        self.database.initSqlCursor()
        self.app = QtGui.QApplication([])
        self.window = TestWindow()

    def run(self):
        self.logger.debug('run()')
        answer = ''
        custom_options = {'end': 10, 'width': 10, 'fill': '#', 'format': '%(progress)s%% [%(fill)s%(blank)s]'}
        try:
            while not answer == '9':
                time.sleep(1)
                if answer == '1':
                    self.window.show()
                    self.app.exec_()
                elif answer == '2':
                    self.database.insertSql('2 was pressed')
                elif answer == '3':
                    self.database.commitSql()
                elif answer == '4':
                    self.database.closeHandle()
                elif answer == '5':
                    pass
                elif answer == '6':
                    pass
                elif answer == '7':
                    pass
                elif answer == '8':
                    p = ProgressBar(** custom_options)
                    for i in range(10):
                        print p + 1
                answer = raw_input("Enter one of the following\r\n\r\n1 -- Window\r\n2 -- database insert\r\n3 -- database commit\r\n4 -- database close handle\r\n5 -- unknown\r\n6 -- unknown\r\n7 -- unknown\r\n8 -- progressbar\r\n9 -- quit\r\n\r\n.....? ")
            self.teardown()
        except Exception, err:
            self.logger.exception('run() ... Exception')
            return 1

    def teardown(self):
        self.logger.info('teardown() ... Quit')
        print "\r\n Exiting Gracefully"

    def handleException(self):
        self.logger.debug('handleException()')
        self.exceptionCount += 1
        trace = traceback.format_exc()
        if self.exceptionCount > 9:
            self.logger.critical('example.py stopped with too many exceptions %s', '%s' % (self.exceptionCount, trace))
            sys.exit(2)
        else:
            self.logger.critical('example.py experienced an unexpected error', '%s' % (trace))

if __name__ == "__main__":

    example = Example()
    example.setup()
    example.run()
    sys.exit(0)
