from threading import Lock

class cert:
    lock = Lock()
    cert_lines = {} # Cache
    def __init__(self, filename: str = 'cert.txt'):
        self.cert_file = open(filename, 'r+', encoding='utf-8')
        self.read()
    def read(self):
        with self.lock:
            self.cert_lines = {}
            self.cert_file.seek(0)
            for row in self.cert_file.readlines():
                cert_row = row.split()
                if not row:
                    continue
                if not len(cert_row) == 3:
                    raise ConnectionError(f'Invaild cert file: line "{row}"')
                self.cert_lines[cert_row[0]] = {'password': cert_row[1], 'level': cert_row[2]}
    def write(self):
        with self.lock:
            cert_text = ''
            for callsign, config_pair in self.cert_lines.items():
                cert_text += f"{callsign} {config_pair['password']} {config_pair['level']}\n"
            self.cert_file.seek(0)
            self.cert_file.write(cert_text)
            self.cert_file.truncate(self.cert_file.tell())
            self.cert_file.flush()
    def __del__(self):
        with self.lock:
            self.cert_file.close()
    def __contains__(self, callsign: str):
        self.read()
        if not callsign in self.cert_lines:
            return False
        return True
    def __setitem__(self, callsign: str, pair: dict):
        if len(pair) > 2 or not 'password' in pair and not 'level' in pair:
            raise SyntaxError('Invaild config pair: '+str(pair))
        elif not callsign in self:
            if not 'level' in pair or not 'password' in pair:
                raise SyntaxError('New callsign must have both "level" and "password" param')
            self.cert_lines[callsign] = {}
        if 'password' in pair:
            self.cert_lines[callsign]['password'] = pair['password']
        if 'level' in pair:
            self.cert_lines[callsign]['level'] = pair['level']
        self.write()
    def __delitem__(self, callsign):
        self.read()
        if not callsign in self:
            raise KeyError(callsign)
        del self.cert_lines[callsign]
        self.write()
    def __getitem__(self, callsign):
        self.read()
        if not callsign in self:
            raise ValueError(callsign)
        return self.cert_lines[callsign]
    def get(self, callsign):
        try:
            return self[callsign]
        except KeyError:
            return None
