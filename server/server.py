# allows to import libs from different dir
import sys, os

# inserts path to access all the libs
sys.path.insert(0, '../libs')

from hashSignVerify import hashFile, createSig, verifySig
from encDec import enc, encFile, decFile

from EncryptedServerSocket import EncryptedServerSocket
# import the client socket to talk to the caServer
from EncryptedSocket import EncryptedSocket
from libs.RSAKeys import genKeyPair
# from RSAKeys import encrypt, decrypt
# from RSAKeys import printEncryptedString
from libs.RSAKeys import readPublicKey, readPrivateKey
from getSert import renewCert
from datetime import datetime, timedelta
import json
from Crypto.PublicKey import RSA


HOST = '127.0.0.1'
PORT = 4443
printDebug = True
certFile = 'cert.txt'

getCert = False

pubKey = readPublicKey()
priKey = readPrivateKey()

SSID = "SecureCanes"

# generate RSA key pair
# if files exist dont generate
if pubKey is None or priKey is None:
  if printDebug:
    print('Generating public and private key')
  genKeyPair()
  pubKey = readPublicKey()
  priKey = readPrivateKey()
  getCert = True
else:
  if printDebug:
    print('Private and public key files found')

if os.path.exists(certFile) and not getCert:
    fl = open(certFile, 'r')
    cert = json.load(fl)
    expiry = datetime.strptime(cert['expiration'], '%Y-%m-%d')
    if expiry <= datetime.now() - timedelta(days=10):
        print(datetime.now() - timedelta(days=10))
        renewCert(pubKey, SSID)
        fl = open(certFile, 'r')
        cert = json.load(fl)
else:
    renewCert(pubKey, SSID)
    fl = open(certFile, 'r')
    cert = json.load(fl)




# open communication with the caServer to obtain certificate
# eSocket = EncryptedSocket(HOST, PORT)

# store the certificate in the given file
# eSocket.storeInFile(certFile)

# close the connection between the caServer
# eSocket.close()

# open server for communication with client
eSocket = EncryptedServerSocket(HOST, PORT)

# send encrypted certificate
eSocket.sendFile(certFile)

# recieve encrypted message
eSocket.storeInFile('response.txt')
CPuk = eSocket.keyChain.externalPubKey
CPuk = RSA.importKey(CPuk)

#-------------------------------------------------
while True:                   #send msg's back and forth between client and server
  passwd = os.urandom(16)     #create passwd, ivval, and salt for new cipher
  ivval = os.urandom(16)
  salt = os.urandom(16)
  blocksize = 16 #? would have to change enc/dec functions as well
                              #initialiize variables, rsa key files and data
  krFname = "privKey.pem"
  kuFname = "pubKey.pem"
  theirData = ""
  #bytes(dataDec)
  dataDec = ""
  #password = "bye"

  #server receives key 1st
  key2 = eSocket.conn.recv(1024)#eSocket.socket.recv(1451)#read() #.socket.recv(1451) #16? 128? something else?
  print('received key\n',key2, end='\n\n')
  k = open(krFname, 'r')                    #decrypt clients key with rsa private key
  prk = RSA.importKey(k.read())
  k.close()
  print("has\n", prk.has_private(), end="\n\n")
  Key2 = prk.decrypt(key2)
  print('key2\n\n',Key2, end='\n')


  #server sends key 2nd         #create aes key
  key, encryptor, padder, iv = enc(passwd, ivval, salt, blocksize)
  Key = CPuk.encrypt(key, 3422)[0]              #encrypt key with clients rsa public key
  eSocket.conn.send(Key, 1024)#eSocket.socket.send(bytes(str(Key), "utf8"))
  print("has\n", CPuk.has_private(), end="\n\n")
  #server receives iv first
  iv2 = eSocket.conn.recv(1024)                 #receive clients iv
  print("iv2\n", iv2, end="\n\n")
  eSocket.conn.send(iv, 1024)                   #send iv
  print("iv sent\n", iv, end="\n\n")


  #while True:
  #server receives msg 1st
  theirData = eSocket.conn.recv(blocksize)
  print("theirData", theirData)
  #while  theirData: #eSocket.conn.recv_into(bytearray(bytes(theirData, "utf8"))) > 0: #bytearray(theirData) = eSocket.socket.recv(blocksize):
  dataDec = decFile(theirData, blocksize, iv2, Key2)  #decrypt msg
  print("dataDec ", dataDec)

  #server sends msg 2nd
  mydata = input("Enter data: ")
  if mydata == "end":                   #server ends msg exchange/loop when they type "end"
    break
  num = 0
  length = len(mydata)
  if length > blocksize:                #to send msg longer than blocksize (is not working yet)
    data = encFile(mydata[num:num+blocksize], encryptor, padder, salt)
    #read file2 and hash and sign
    #sig = createSig(data, krFname, password, blocksize) 
    num += blocksize
    eSocket.conn.send(data)             #send encrypted msg
  else:
    data = encFile(mydata[num:num+length], encryptor, padder, salt) 
    num += length
    eSocket.conn.send(data)

  #-------------------------------------------
  
# close connection with client
eSocket.close()

