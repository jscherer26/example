import sys, os
import sqlite3

class DbSqlite3(object):

    def __init__(self, parent, database = None):

        self.parent = parent
        self.parent.logger.info('__init__()')
        self.database = None

        self.sqlConnection = None
        self.sqlCursor = None
        
        self.setDatabase(database)
        self.initSqlCursor()

    def initSqlCursor(self):

        if not os.path.exists(os.path.dirname(self.database)):
            self.parent.logger.error('setDatabase() ... Error Path >>%s<< does not exist' % (os.path.dirname(self.database)))
            sys.exit(1)

        existsDb = os.path.exists(self.database)

        self.sqlConnection = sqlite3.connect(self.database)
        self.sqlCursor = self.sqlConnection.cursor()

        if not existsDb:
            self.createDbTables()

    def setDatabase(self, database):

        self.parent.logger.debug('setDatabase() ... Set Database >>%s<<' % (database))
        self.database = database

    def createDbTables(self):

        self.parent.logger.warning('createDbTables() ... Database >>%s<< does not exist ... creating it' % (os.path.basename(self.database)))
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
            self.parent.logger.exception('example.run()')


    def insertSql(self, message):

        self.parent.logger.debug('insertSQL() .. Insert Message >>%s<<' % (message))
        self.sqlCursor.execute('INSERT INTO example1 (message) VALUES (?)', (message,))

    def commitSql(self):

        self.parent.logger.debug('commitSQL()')
        self.sqlConnection.commit()

    def closeHandle(self):

        self.parent.logger.debug('closeHandle()')
        self.sqlConnection.close()

