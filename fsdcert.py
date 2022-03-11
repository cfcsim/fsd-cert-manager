import os, re, time

if not os.path.isfile('cert.txt'):
    raise FileNotFoundError('There is not cert.txt, please check')

class logger:
    def info(msg):
        print(msg)

lock = False # Processing lock

'''
Style of API: RESTful API
'state' param explain:
    1: OK
    2: User already exist
    3: User doesn't exist
    4: Key wrong
'''

# Build line or convert line to list
def linebuild(obj):
    if isinstance(obj, list):
        return obj[0]+' '+obj[1]+' '+str(obj[2])
    elif isinstance(obj, str):
        return obj.split()
    return False

# Search line by callsign
def search(certfile, callsign):
    lines = certfile.readlines()
    for line in lines:
        if line.split()[0] == callsign:
            return line
    return False

# /userinfo?callsign=
def query(callsign):
    global lock
    while lock:
        pass
    lock = True
    with open('cert.txt', 'r') as certfile:
        result = linebuild(search(certfile, callsign))
        if not result:
            logger.info("Queried "+callsign+", doesn't exist")
            lock = False
            return False
        priv = result[2]
        logger.info("Queried "+callsign+", exist, authority: "+priv)
        lock = False
        return int(priv)

def create(callsign, password):
    global lock
    while lock:
        pass
    if type(query(callsign)) == int:
        logger.info("Try create "+callsign+", already exist")
        return False
    lock = True
    with open('cert.txt', 'a') as certfile:
        certfile.write(linebuild([callsign, password, 1])+'\n')
        logger.info("Created "+callsign)
        lock = False
        return True

# Modify user (e.g. password, priv......
def modify(callsign, newpwd=None, newpriv=None):
    global lock
    while lock:
        pass
    if not newpwd and not type(newpriv) == int:
        return False
    if not type(query(callsign)) == int:
        logger.info("Try change password, "+callsign+" doesn't exist")
        return False
    lock = True
    with open('cert.txt', 'r') as certfile:
        oldline = search(certfile, callsign)
        data = linebuild(oldline)
        if newpwd:
            data[1] = newpwd
        if newpriv or newpriv == 0:
            data[2] = newpriv
        newline = linebuild(data)+'\n'
        certfile.seek(0)
        text = certfile.read()
    with open('.newcert.txt', 'w') as certfile:
        certfile.write(text.replace(oldline, newline))
    os.remove('cert.txt')
    os.rename('.newcert.txt', 'cert.txt')
    lock = False
    return True

def login(callsign, password):
    global lock
    while lock:
        pass
    if not type(query(callsign)) == int:
        return False
    lock = True
    with open('cert.txt', 'r') as certfile:
        line = linebuild(search(certfile, callsign))
        rpassword = line[1]
        if not int(line[2]):
            return False
        lock = False
        if password == rpassword:
            return int(line[2])
        else:
            return False
        
def whazzup():
    logger.info("Get whazzup")
    try:
        with open('whazzup.txt', 'r') as whazzupfile:
            return whazzupfile.read()
    except:
        return '!whazzup.txt not exist or cannot read, please check'

