import socket
from KeyChain import KeyChain
from communication import sendEncData, readEncData
from communication import sendEncFile, storeEncFile

printDebug = True

# this class defines an encrypted socket for a client
class EncryptedServerSocket:
  def __init__(self, host, port):
    # this stores the RSA keys for encrypted communication
    self.keyChain = KeyChain()
    # store the host and port
    self.host = host
    self.port = port
    # init the socket
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind to the host and the port
    self.socket.bind((self.host, self.port))
    # opening the port for listening
    self.socket.listen()
    self.conn, self.addr = self.socket.accept()
    if printDebug:
      print('Connected by', self.addr)

    # setup encrypted communication
    # send public key to client
    self.keyChain.sendPubKey(self.conn)
    # recieve clients public key
    self.keyChain.readPubKey(self.conn)

  # close the socket
  def close(self):
    self.conn.close()

  # send encrypted message
  def send(self, message):
    sendEncData(self.conn, message, self.keyChain.externalPubKey)

  # read encrypted message
  def read(self):
    return readEncData(self.conn, self.keyChain.priKey)

  # send encrypted file
  def sendFile(self, fileName):
    sendEncFile(self.conn, fileName, self.keyChain.externalPubKey)

  # store the comminication to a file
  # if append is not none the contents will be appended to the file
  def storeInFile(self, fileName, append = None):
    storeEncFile(self.conn, fileName, self.keyChain.priKey, append)
