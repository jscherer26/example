import os, sys
import unittest
import logging

from src.db import DbSqlite3

class SetDatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.level = logging.CRITICAL
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.dbTestFile = '../files/test.db'
        self.database = DbSqlite3(self, self.dbTestFile)
        self.database.initSqlCursor()
    def tearDown(self):
        self.database.closeHandle()
        if os.path.exists(self.dbTestFile):
            os.remove(self.dbTestFile)
        self.database = None
        self.logger = None
    def testSetDatabase(self):
        changeFile = '../files/change.db'
        self.database.setDbFile(changeFile)
        self.assertEqual(changeFile, self.database.dbFile, 'Database Name did not change')
        self.database.setDbFile(self.dbTestFile)
        self.assertEqual(self.dbTestFile, self.database.dbFile, 'Database Name did not reset')
    def testInitSqlCursor(self):
        self.database.closeHandle()
        if os.path.exists(self.dbTestFile):
            os.remove(self.dbTestFile)
        self.database.initSqlCursor()
        self.assertTrue(os.path.exists(self.dbTestFile), 'Database File Does NOT Exist')
    def testCreateDbTables(self):
        self.database.createDbTables()
        self.database.sqlCursor.execute('''select name from sqlite_master where type = 'table';''')
        self.assertEqual(tuple(self.database.sqlCursor.fetchall()), ((u'example1',), (u'sqlite_sequence',)))
        self.database.sqlCursor.execute('''select sql from sqlite_master where type = 'table' and name = 'example1';''')
        self.assertEqual(tuple(self.database.sqlCursor.fetchall()),
            ((u'CREATE TABLE example1 (\n            Id INTEGER PRIMARY KEY AUTOINCREMENT,\n            creDT DATE,\n            updDT DATE,\n            message TEXT)',),))
    def testInsertSql(self):
        self.database.createDbTables()
        self.database.sqlCursor.execute('''select * from example1 where message = '1st Insert';''')
        self.assertTrue(True if not self.database.sqlCursor.fetchall() else False)
        self.database.insertSql('1st Insert')
        self.database.sqlCursor.execute('''select * from example1 where message = '1st Insert';''')
        self.assertFalse(True if not self.database.sqlCursor.fetchall() else False)
    def testCommitSql(self):
        self.database.createDbTables()
        self.database.sqlCursor.execute('''select * from example1 where message = '1st Insert';''')
        self.assertTrue(True if not self.database.sqlCursor.fetchall() else False)
        self.database.insertSql('1st Insert')
        self.database.sqlCursor.execute('''select * from example1 where message = '1st Insert';''')
        self.assertFalse(True if not self.database.sqlCursor.fetchall() else False)
        self.database.closeHandle()
        self.database.initSqlCursor()
        self.database.sqlCursor.execute('''select * from example1 where message = '1st Insert';''')
        self.assertTrue(True if not self.database.sqlCursor.fetchall() else False)
        self.database.commitSql()
        self.database.closeHandle()
        self.database.initSqlCursor()
        self.database.sqlCursor.execute('''select * from example1 where message = '1st Insert';''')
        self.assertTrue(True if not self.database.sqlCursor.fetchall() else False)
    def testCloseHandle(self):
        isHandle = True
        try:
            self.database.sqlCursor.execute('''select * from example1 where message = '1st Insert';''')
        except:
            isHandle = False
        self.assertTrue(isHandle)
        self.database.closeHandle()
        isHandle = True
        try:
            self.database.sqlCursor.execute('''select * from example1 where message = '1st Insert';''')
        except:
            isHandle = False
        self.assertFalse(isHandle)
