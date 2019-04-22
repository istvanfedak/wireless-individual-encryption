printDebug = True

from RSAKeys import encrypt, decrypt

def sendData(socket, message):
  if printDebug:
    print('\n\nSending the following message:')
    print('message length =', len(message))
    print('--------------------------------------------------------------------------------')
    print(message, end='\n\n')
  socket.send(message.encode('utf-8'))

# reading all of the data from the socket
def readData(socket):
  # keeps track of the entire packet contents
  message = ''
  # keeps track of the total message size
  recvd = 0

  while True:
    # recieves a message of size 512
    submess = socket.recv(512).decode('utf-8')
    # appends the message to packet
    message += submess
    # appends the size of the message recieved
    recvd += len(submess)
    # if the message size is less than 512 break
    if len(submess) < 512:
        break
  if printDebug:
    print('\n\nRecieved the following message:')
    print('message length =', recvd)
    print('--------------------------------------------------------------------------------')
    print(message, end='\n\n')
  return message

# send encrypted data
def sendEncData(socket, message, pubKey):
  if printDebug:
    print('\n\nEncrypting and sending the following message:')
    print('message length =', len(message))
    print('--------------------------------------------------------------------------------')
    print(message, end='\n\n')
  # iterate through the entire size of the string
  while True:
    # if the message is less than 512 just send it
    if len(message) < 512:
      # send encrypted message
      socket.send(encrypt(message.encode('utf-8'), pubKey)[0])
      break
    # if its not, send substring and delete the substring from message
    else:
      submess = message[0:512]
      socket.send(encrypt(submess.encode('utf-8'), pubKey)[0])
      # remove substring from message
      message = message[512:]

# recieve encrypted data
def readEncData(socket, priKey):
  # keeps track of the entire packet contents
  message = ''
  # keeps track of the total message size
  recvd = 0

  while True:
    # recieves a message of size 512
    submess = socket.recv(512)
    submess = decrypt(submess, priKey).decode('utf-8')
    # appends the message to packet
    message += submess
    # appends the size of the message recieved
    recvd += len(submess)
    # if the message size is less than 512 break
    if len(submess) < 512:
        break
  if printDebug:
    print('\n\nDecrypted and recieved the following message:')
    print('message length =', recvd)
    print('--------------------------------------------------------------------------------')
    print(message, end='\n\n')
  return message

# send an ecrypted file across a socket
def sendEncFile(socket, fileName, pubKey):
  with open(fileName, 'r') as fd:
    sendEncData(socket, fd.read(), pubKey)
    fd.close()

'''
# this code shows how to handle if the file wasn't found
try:
  fd = open(fileName)
except FileNotFoundError:
  print('file not found')
'''

# store encrypted file
def storeEncFile(socket, fileName, priKey, append = None):
  if append is None:
    with open(fileName, 'w') as fd:
      message = readEncData(socket, priKey)
      fd.write(message)
      fd.close()
  # if append is not None then append to the file
  else:
    with open(fileName, 'a') as fd:
      message = readEncData(socket, priKey)
      fd.write(message)
      fd.close()


def sendEncrypted(socket, message, pubKey):
  sendEncData(socket, message, pubKey)


def recvEncrypted(socket, priKey):
  readEncData(socket, priKey)

