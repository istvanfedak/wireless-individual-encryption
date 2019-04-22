from libs.RSAKeys import genKeyPair
from libs.RSAKeys import readPublicKey, readPrivateKey
from communication import sendData, readData
printDebug = False

# this class stores the RSA public and private keys
class KeyChain:
  def __init__(self):
    # reads in its own public and private keys
    self.pubKey = readPublicKey()
    self.priKey = readPrivateKey()

    # sets up the parameter for the others public key
    externalPubKey = None

    # generate RSA key pair
    # if files exist dont generate
    if self.pubKey is None or self.priKey is None:
      if printDebug:
        print('Generating public and private key')
      genKeyPair()
      self.pubKey = readPublicKey()
      self.priKey = readPrivateKey()
    else:
      if printDebug:
        print('Private and public key files found')

  # sends the public key through socket
  def sendPubKey(self, socket):
    if printDebug:
      print('\nSending the following server public key:')
      print('--------------------------------------------------------------------------------\n')
      print(self.pubKey, end='\n\n')

    # send unsigned public key to client
    sendData(socket, self.pubKey)

  # recieve external public key from socket
  def readPubKey(self, socket):
    # read the public key from socket
    self.externalPubKey = readData(socket)
    if printDebug:
      print('\nRecieved the following external public key')
      print('--------------------------------------------------------------------------------\n')
      print(self.externalPubKey, end='\n\n')
