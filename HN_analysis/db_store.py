import sqlite3 as sq3

class SQLCursor():

    def cleanup(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def open(self):
        try:
            self.connection = sq3.connect(self.filename)
            self.cursor = self.connection.cursor()
        except:
            self.cleanup()

    def __init__ (self, filename):
        self.filename = filename
        self.connection = None
        self.cursor = None

    def __enter__ (self):
        self.open()
        return self

    def __exit__(self, *args):
        self.cleanup()

    def execute(self, query):
        return self.cursor.execute(query)

    def executemany(self, query, argtab):
        return self.cursor.executemany(query, argtab)

    def getcursor(self):
        return self.cursor

    def getconnection(self):
        return self.connection
