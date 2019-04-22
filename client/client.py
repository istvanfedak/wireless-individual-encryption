# allows to import RSA lib from different dir
import sys, json, os

# inserts path to access all the libs
sys.path.insert(0, '../libs')

from hashSignVerify import hashFile, createSig, verifySig
from encDec import enc, encFile, decFile

from RSAKeys import encrypt, decrypt

from EncryptedSocket import EncryptedSocket
from verify import verify

from Crypto.PublicKey import RSA
from cryptography.hazmat.primitives import serialization

HOST = '127.0.0.1'
PORT = 4443
printDebug = True

certFile = 'certificates.json'

# read database of certificates
# certificates = Certificates(certFile)

# connect to the server
eSocket = EncryptedSocket(HOST, PORT)

# read the certificate from the server
cert = eSocket.read()

if printDebug:
  print(cert)

cert = json.loads(cert)
APPuk = cert['pubKey']
print("public key", APPuk, end='\n\n')
APPuk = RSA.importKey(APPuk)
print('server pubkey\n\n',APPuk,end='\n\n')


# try to find certificate in certificates
if verify(cert):
  # send encrypted message
  eSocket.send('So now what?!')
else:
  # send encrypted message
  eSocket.send('Go away!')
  exit()

#-------------------------------------------------
while True:
  passwd = os.urandom(16)
  ivval = os.urandom(16)
  salt = os.urandom(16)
  blocksize = 16  #1024  #512? would have to change enc/dec functions as well

  krFname = "privKey.pem"
  kuFname = "pubKey.pem"
  theirData = ""
  #bytes(dataDec)
  dataDec = ""
  #password = "hello"
  

  #client sends key 1st
  k = open(krFname, 'r')
  prk = RSA.importKey(k.read())
  k.close()
  key, cipher, padder, iv = enc(passwd, ivval, salt, blocksize)
  print("key \n", key, end="\n\n")
  Key = APPuk.encrypt(key, 3422)[0]
  print("Key", Key, end="\n\n")
  print("has\n", APPuk.has_private(), end="\n\n")
  print(len(Key))
  eSocket.socket.send(Key,1024)
  print("aes key sent with rsa public key")


  #cleint receives key 2nd
  key2 = eSocket.socket.recv(1024)#read() #socket.recv(16) #?is actually 512
  print("key2", key2, end="\n\n")
  Key2 = prk.decrypt(key2)
  print("has\n", prk.has_private(), end="\n\n")
  print('key2\n\n',Key2, end='\n')

  #sends iv first, then reeceives
  eSocket.socket.send(iv,1024)
  print("iv sent\n", iv, end="\n\n")
  iv2 = eSocket.socket.recv(1024)
  print("iv2\n", iv2, end="\n\n")


  #while True:
  #client sends first
  mydata = input("Enter data: ")
  if mydata == "end":
    break
  num = 0
  length = len(mydata)
  if length > blocksize:        
    data = encFile(mydata[num:num+blocksize], cipher, padder, salt) 
    num += blocksize
    print("Data ", data)
    eSocket.socket.send(data)
  else:
    data = encFile(mydata[num:num+length], cipher, padder, salt) 
    num += length
    print("Data ", data)
    eSocket.socket.send(data)

  #client receives 2nd
  theirData = eSocket.socket.recv(blocksize)
  #while theirData:#eSocket.socket.recv_into(bytearray(theirData)) > 0: #bytearray(theirData) = eSocket.socket.recv(blocksize):
  dataDec = decFile(theirData, blocksize, iv2, Key2)
  print(dataDec)

#-------------------------------------------

# close socket
eSocket.close()

