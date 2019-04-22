from Crypto.PublicKey import RSA
from Crypto import Random
from settings import PRIVATE_KEY, PUBLIC_KEY
import base64

printDebug = False

# this functon prints an encrypted message
def printEncryptedString(string):
  i = 0
  for i in range(0, len(string), 20):
    print(string[i:i+20])
    i += 1
  print(end='\n\n')

# this function reads the generated privet key and returns it as a string
def readPrivateKey():
  try:
    fd = open(PRIVATE_KEY, 'r')
    return fd.read()
  except FileNotFoundError:
    return None

# this function reads the generated public key and returns it as a string
def readPublicKey():
  try:
    fd = open(PUBLIC_KEY, 'r')
    return fd.read()
  except FileNotFoundError:
    return None

def genKeyPair():
  key = RSA.generate(4096, Random.new().read)

  priv = key.exportKey()
  pub = key.publickey().exportKey()

  if printDebug:
    print(priv.decode('utf-8'))
  fd = open(PRIVATE_KEY, 'wb')
  fd.write(priv)
  fd.close()

  if printDebug:
    print(pub.decode('utf-8'))
  fd = open(PUBLIC_KEY, 'wb')
  fd.write(pub)
  fd.close()

def encrypt(text, key):
  print('key', key)
  key = RSA.importKey(key)
  encrypted = key.encrypt(text, 3422)
  if printDebug:
    printEncryptedString(encrypted[0])
  return encrypted

def decrypt(encrypted, key, isString = True):
  if isString:
      encrypted_message = base64.b64decode(encrypted)
  else:
      encrypted_message = encrypted
  key = RSA.importKey(key)
  decrypt = key.decrypt(encrypted_message)
  if printDebug:
    print(decrypt)
  return decrypt
