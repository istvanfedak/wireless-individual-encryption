# allows to import libs from different dir
import sys

# inserts path to access all the libs
sys.path.insert(0, '../libs')

# from EncryptedServerSocket import EncryptedServerSocket
from libs.EncryptedServerSocket import EncryptedServerSocket
# imports the library that allows it to create new certificates
from signAP import newCert

# CONSTANTS
HOST = '127.0.0.1'
APNAME = 'SecureCanesGuest'
PORT = 4444
printDebug = True

def runCA():
    # open server for communication
    eSocket = EncryptedServerSocket(HOST, PORT)

    SSID = eSocket.read()

    if printDebug:
        print('SSID Received:', SSID)

    # generate a new certificate using the public key of the caServer
    # the encrypted socket already stores it in a keychain
    cert = newCert(SSID, eSocket.keyChain.externalPubKey)

    # send encrypted certificate to server
    eSocket.send(cert)

    # close socket
    eSocket.close()