import sys

sys.path.insert(0, '../libs')

from libs import EncryptedServerSocket
from libs import EncryptedSocket
from db import db
import re

db = db.Database()

class SSIDExists(Exception):
    pass


def listenOthers():
    print("Starting to listen for requests from CAs")
    while True:
        eServer = EncryptedServerSocket.EncryptedServerSocket('localhost', 5467)
        SSIDHashed = eServer.read()
        try:
            for cert in db.db.data['certs']:
                if cert['hashedSSID'] == SSIDHashed:
                    eServer.send('yes')
                    eServer.close()
                    raise SSIDExists()
        except SSIDExists:
            continue
        eServer.send('no')
        eServer.close()


def verifyOthers(SSIDHashed):
    trustedList = db.db.data['trustedCAs']
    failed = 0

    for ca in trustedList:
        p = '(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
        m = re.search(p, ca)
        host = m.group('host')
        port = m.group('port')
        print(host, port)
        try:
            eSocket = EncryptedSocket.EncryptedSocket(host, int(port))
            eSocket.send(SSIDHashed)
            response = eSocket.read()
            if response == 'yes':
                return False
        except ConnectionRefusedError:
            print("cant connect")
            failed += 1
        if failed / len(trustedList) > 0.3:
            return False
    return True
