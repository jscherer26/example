import sys, os
import logging
import sqlite3

class DbSqlite3(object):

    def __init__(self, dbFile):

        self.logger = logging.getLogger('root')
        self.logger.info('__init__()')
        self.dbFile = dbFile

        self.sqlConnection = None
        self.sqlCursor = None

    def initSqlCursor(self):

        if not os.path.exists(os.path.dirname(self.dbFile)):
            self.logger.error('setDbfile() ... Error Path >>%s<< does not exist' % (os.path.dirname(self.dbFile)))
            sys.exit(1)

        existsDb = os.path.exists(self.dbFile)

        self.sqlConnection = sqlite3.connect(self.dbFile)
        self.sqlCursor = self.sqlConnection.cursor()

        if not existsDb:
            self.createDbTables()

    def setDbFile(self, dbFile):

        self.logger.debug('setDbFile() ... Set Database File >>%s<<' % (dbFile))
        self.dbFile = dbFile

    def createDbTables(self):

        self.logger.warning('createDbTables() ... Database >>%s<< does not exist ... creating it' % (os.path.basename(self.dbFile)))
        try:
            self.sqlCursor.execute("""
            CREATE TABLE example1 (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            creDT DATE,
            updDT DATE,
            message TEXT)
            """)
            
            self.sqlCursor.execute("""
            CREATE TRIGGER insert_example1_creDT
            AFTER INSERT ON example1
            BEGIN
            UPDATE example1 SET creDT = DATETIME('now','localtime') WHERE rowid = new.rowid;
            END;
            """)
    
            self.sqlCursor.execute("""
            CREATE TRIGGER update_example1_updDT
            AFTER UPDATE ON example1
            BEGIN
            UPDATE example1 SET updDT = DATETIME('now','localtime') WHERE rowid = new.rowid;
            END;
            """)
        except Exception, err:
            self.logger.exception('example.run()')


    def insertSql(self, message):

        self.logger.debug('insertSQL() .. Insert Message >>%s<<' % (message))
        self.sqlCursor.execute('INSERT INTO example1 (message) VALUES (?)', (message,))

    def commitSql(self):

        self.logger.debug('commitSQL()')
        self.sqlConnection.commit()

    def closeHandle(self):

        self.logger.debug('closeHandle()')
        self.sqlConnection.close()

