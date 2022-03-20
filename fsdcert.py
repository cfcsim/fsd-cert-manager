import sqlite3

class create_cert:
    def __init__(self, dbname='cert.sqlitedb3', tablename='cert'):
        self.__dbconn = sqlite3.connect(dbname)
        self.__dbcurs = self.__dbconn.cursor()
        self.__dbname = tablename

    def __del__(self):
        self.__dbconn.commit()
        self.__dbconn.close()
        del self.__dbconn
        del self.__dbcurs
        del self.__dbname
        del self

    def __contains__(self, callsign):
        try:
            c = self.__dbcurs.execute("SELECT * FROM %s WHERE callsign='%s';" % (self.__dbname, callsign))
        except:
            return False
        for _ in c:
            return True
        return False

    def __setitem__(self, callsign, pair):
        if callsign in self:
            if 'password' in pair:
                self.__dbcurs.execute("UPDATE %s SET password = '%s' WHERE callsign = '%s'" % (self.__dbname, pair['password'], callsign))
            if 'level' in pair:
                self.__dbcurs.execute("UPDATE %s SET level = '%i' WHERE callsign = '%s'" % (self.__dbname, pair['level'], callsign))
            self.__dbconn.commit()
            return
        self.__dbcurs.execute("INSERT INTO %s VALUES (?, ?, ?)" % self.__dbname, (callsign, pair['password'], pair['level']))
        self.__dbconn.commit()
    
    def __delitem__(self, callsign):
        if not callsign in self:
            raise KeyError(callsign)
        self.__dbcurs.execute("DELETE FROM %s WHERE callsign='%s'" % (self.__dbname, callsign))
        self.__dbconn.commit()

    def __getitem__(self, callsign):
        try:
            c = self.__dbcurs.execute("SELECT * FROM %s WHERE callsign='%s';" % (self.__dbname, callsign))
        except:
            raise KeyError(callsign)
        for r in c:
            return {'level': r[2]}
        raise KeyError(callsign)

    def get(self, callsign):
        try:
            return self[callsign]
        except KeyError:
            return None
