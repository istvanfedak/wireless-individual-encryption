# allows to import RSA lib from different dir
import sys
import json
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from libs import RSAKeys
import binascii
from datetime import datetime

# inserts path to access all the libs
sys.path.insert(0, '../libs')

# keychain stores all the RSA keys
from KeyChain import KeyChain

# import decrypt fucntion to verify key
from RSAKeys import decrypt

caPubKeyFile = 'certificate_public.pem'
printDebug = True

# this function has all the logic to verify a certificate
def verify(cert):
  hash = cert['signedHash']
  SSID = cert['SSID']
  print(SSID)
  # need to convert to date
  expiration = cert['expiration']
  datetime_expiration = datetime.strptime(expiration, '%Y-%m-%d').date()
  # print(datetime_expiration)
  pubKey = cert['pubKey']
  ca = cert['ca']
  caKey = open('certificate_public.pem', 'r')
  # caKey = RSA.importKey(caKey.read())
  verCert = {
    'SSID': SSID,
    'expiration': datetime_expiration.isoformat(),
    'pubKey': pubKey,
    'ca': ca,
  }
  print(verCert)
  # cert['expiration'] = cert['expiration'].isoformat()
  jsData = json.dumps(verCert)
  verHash = SHA256.new(jsData.encode('utf-8')).digest()
  print(hash)
  hexlified = "b'" + str(hash) + "'"
  print(verHash)
  print(hexlified)
  # hash = binascii.unhexlify(hash)
  print(hash)

  pubKey = caKey.read()
  pubKey = RSA.importKey(pubKey)
  hash = (int(hash[1:-2]),)
  return pubKey.verify(verHash, hash)

  # hash = RSAKeys.decrypt(hash, pubKey)
  # print(hash)
  # print(verHash)
  # return True

