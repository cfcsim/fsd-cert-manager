import re

class logger:
    def info(info):
        pass

def search(file, word):
    while True:
        text = file.readline()
        if text.split()[0] == word:
            return text
            break
        
def query(name):
    with open('cert.txt', 'r') as certfile:
        cert = certfile.read()
        tuple = re.search('\n'+name, cert)
        if tuple == None:
            logger.info("Queried: "+name+", not exist")
            return { "status": 200, "exist": False }
    with open('cert.txt', 'r') as certfile:
        authty = search(certfile, name).split()[2]
        logger.info("Queried: "+name+", exist, authority: "+authty)
        return { "status": 200, "exist": True, "authty": authty }

def create(name, passwd):
    if query(name)['exist']:
        logger.info("Try create: "+name+", name exist")
        return { "status": 409, "msg": "User already exist" }
    with open('cert.txt', 'a') as certfile:
        certfile.write(name+" "+passwd+" 1\n")
        logger.info("Try create: "+name+", success")
        return { "status": 200, "msg": "Success created" }

def changepwd(name, newpwd):
    if not query(name)['exist']:
        logger.info("Try change password")
        return { "status": 404, "msg": "User not found" }
    with open('cert.txt', 'r') as certfile:
        cert = certfile.read()
    with open('cert.txt', 'r') as certfile:
        fullcont = search(certfile, name)
    cont = fullcont.split(" ")
    modcont = cont[0]+" "+newpwd+" "+cont[2]
    modcert = cert.replace(fullcont, modcont)
    with open('cert.txt', 'w') as certfile:
        certfile.write(modcert)
    return { "status": 200, "msg": "Success changed" }

def changeauth(name, newauth):
    if not query(name)['exist']:
        return { "status": 404, "msg": "User not found" }
    with open('cert.txt', 'r') as certfile:
        cert = certfile.read()
    with open('cert.txt', 'r') as certfile:
        fullcont = search(certfile, name)
    cont = fullcont.split(" ")
    modcont = cont[0]+" "+cont[1]+" "+newauth+"\n"
    modcert = cert.replace(fullcont, modcont)
    with open('cert.txt', 'w') as certfile:
        certfile.write(modcert)
    return { "status": 200, "msg": "Success changed" }

def checkauth(name, password):
    if not query(name)['exist']:
        return { "status": 200, "right": "no" }
    with open('cert.txt', 'r') as certfile:
        rpassword = search(certfile, name).split()[1]        
        if not password == rpassword:
            return { "status": 200, "right": "no" }
        else:
            return { "status": 200, "right": "yes" }
        
def whazzup():
    logger.info("Get whazzup")
    with open('whazzup.txt', 'rb') as whazzupfile:
        return whazzupfile.read()

