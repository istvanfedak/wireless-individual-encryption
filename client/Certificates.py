# this class is used by the client to store all the certificates

import json

printDebug = True

# TODO actually verify the certificate using the pubkey of the CaServer

class Certificates:
  # file name is the name of the json certificates file
  def __init__(self, certFileName):
    self.certFileName = certFileName

    # read database of certificates
    with open(certFileName, 'r') as fin:
      self.certificates = json.load(fin)
      # make sure that file exists
      if self.certificates is None :
        raise ValueError()

  # verify that the certificate exists
  def verify(self, cert):
    # try to find certificate in certificates
    try:
      value = self.certificates[cert]
      return True

    # if value not found notify user
    except KeyError:
      if printDebug:
        print('certificate not found')
      return False
