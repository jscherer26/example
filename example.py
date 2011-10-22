#!\usr\bin\python

import sys, time, cStringIO
import logging.config
import yaml

import src.myTraceback as traceback
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
        self.progressBar = None

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
        custom_options = {'end': 10, 'width': 10, 'fill': '#', 'format': '%(progress)s%% [%(fill)s%(blank)s]'}
        self.progressBar = ProgressBar(** custom_options)

    def run(self):
        answer = ''
        try:
            while not answer == '9':
                time.sleep(1)
                if answer == '1':
                    self.window.show()
                    self.app.exec_()
                elif answer == '2':
                    self.database.insertSql('insert into database')
                elif answer == '3':
                    self.database.commitSql()
                elif answer == '4':
                    self.database.closeHandle()
                elif answer == '5':
                    (x, y) = (5, 0)
                    a = x / y
                elif answer == '6':
                    self.logger.error('run() ... Error')
                elif answer == '7':
                    self.logger.warning('run() ... Warning')
                elif answer == '8':
                    if self.progressBar == 100:
                        self.progressBar.reset()
                    print self.progressBar + 1
                answer = raw_input("\r\n\r\nEnter one of the following\r\n\r\n1 -- Window\r\n2 -- database insert\r\n3 -- database commit\r\n4 -- database close handle\r\n5 -- Critical\r\n6 -- Error\r\n7 -- Warning\r\n8 -- progressbar\r\n9 -- quit\r\n\r\n.....? ")
                self.logger.debug('run() ... selection >>%s<<' % (answer))
            self.teardown()
        except Exception:
            self.logger.critical('run() ... Exception \r\n\r\n %s', traceback.format_exc(with_vars = True))

    def teardown(self):
        self.logger.info('teardown() ... Quit')
        print "\r\n Exiting Gracefully"

if __name__ == "__main__":

    example = Example()
    example.setup()
    example.run()
    sys.exit(0)
