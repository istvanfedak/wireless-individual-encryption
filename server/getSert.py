# allows to import RSA lib from different dir
import sys

# inserts path to access RSA encryption lib
# sys.path.insert(0, '../RSAEncryption')

import socket
import json

from libs.communication import sendEncrypted, recvEncrypted, sendData, readData
from libs.RSAKeys import readPrivateKey
from libs.EncryptedSocket import EncryptedSocket
from libs.settings import *

HOST = '127.0.0.1'
PORT = 4444
printDebug = True
SSID = "SecureCanes"

def readData(conn):
  packetFile = open("packetText.txt", mode = 'a+')
  recvd = 0
  while True:
    mess = conn.recv(512).decode('utf-8')
    if len(mess) < 512:
        packetFile.write(mess)
        break
    recvd += len(mess)
    packetFile.write(mess)
# packetFile.close()
#packetFile = open("packetText.txt", mode = 'r')
  serverData = packetFile.read(recvd)
  return serverData

# sending data
def sendData(conn, data):
  dataFile = open("sendData.txt", mode = 'a+')
  dataFile.write(data)
  while True:
    packet = dataFile.read(512)
    if len(packet) < 512:
      conn.send(packet.encode('utf-8'))
      sent += len(packet)
      dataFile.close()
      break
    sent += len(packet)
    conn.send(packet.encode('utf-8'))
  return sent


def renewCert(pubKey, SSID):
  # Encrypted Sockets
  s = EncryptedSocket(HOST, PORT)

  # send SSID
  s.send(SSID)

  # receive certificate
  cert = s.read()
  fl = open(CERT_FILE, 'w+')
  fl.write(cert)

  s.close()



