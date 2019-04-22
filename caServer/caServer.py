import os, RSAKeys, settings
from db import db
from Crypto.PublicKey import RSA
import caSettings, myCaServer, interCA
import threading

if not (os.path.exists(settings.PUBLIC_KEY) and os.path.exists(settings.PRIVATE_KEY)):
    try:
        RSAKeys.genKeyPair()
    except PermissionError:
        print("Permission error, cant create certificate files")
        exit(1)

if not (os.path.exists(caSettings.PUBLIC_KEY) and os.path.exists(caSettings.PRIVATE_KEY)):
    try:
        RSAKeys.genKeyPair(caSettings.PUBLIC_KEY, caSettings.PRIVATE_KEY)
    except PermissionError:
        print("Permission error, cant create certificate files")
        exit(1)

fl = open(settings.PUBLIC_KEY, 'rb')
privKey = RSA.importKey(fl.read())
fl.close()

fl = open(settings.PRIVATE_KEY, 'rb')
pubKey = RSA.importKey(fl.read())
fl.close()

dbdb = db.Database()
db = dbdb.db.data

# db.update({
#     'trustedCAs': ['localhost:1224'],
# })
# dbdb.save()
# db.update({
#     'certs': {'init': []}
# })

print(db)

t1 = threading.Thread(target=interCA.listenOthers)
t1.start()

myCaServer.runCA()

