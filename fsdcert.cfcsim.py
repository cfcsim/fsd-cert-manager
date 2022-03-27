import sqlite3

class cert:
    def __init__(self, dbname='cert.sqlitedb3', tablename='cert'):
        self.db_cursor = sqlite3.connect(dbname).cursor()
        self.table_name = tablename
    def __del__(self):
        self.db_cursor.connection.commit()
        self.db_cursor.connection.close()
    def __contains__(self, callsign):
        for _ in self.db_cursor.execute(
            f"SELECT callsign FROM {self.table_name} WHERE callsign='{callsign}';"
        ):
            return True
        return False
    def __setitem__(self, callsign, pair):
        if callsign in self:
            if 'password' in pair:
                self.db_cursor.execute(
                    f"UPDATE {self.table_name} SET password = '{pair['password']}' WHERE callsign = '{callsign}';"
                )
            if 'level' in pair:
                self.db_cursor.execute(
                    f"UPDATE {self.table_name} SET level = '{pair['level']}' WHERE callsign = '{callsign}';"
                )
            self.db_cursor.connection.commit()
            return
        self.db_cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?);",
            (callsign, pair['password'], pair['level'])
        )
        self.db_cursor.connection.commit()
    def __delitem__(self, callsign):
        if not callsign in self:
            raise KeyError(callsign)
        self.db_cursor.execute(f"DELETE FROM {self.table_name} WHERE callsign='{callsign}';")
        self.db_cursor.connection.commit()
    def __getitem__(self, callsign):
        for row in self.db_cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE callsign='{callsign}';"
        ):
            return {'level': row[2], 'password': row[1]}
        raise KeyError(callsign)
    def get(self, callsign):
        try:
            return self[callsign]
        except KeyError:
            return None
