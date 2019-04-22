from Crypto.PublicKey import RSA
from Crypto import Random
from libs.settings import PRIVATE_KEY, PUBLIC_KEY


def genKeyPair(pubKeyName = PUBLIC_KEY, privKeyName = PRIVATE_KEY):
    key = RSA.generate(4096, Random.new().read)

    priv = key.exportKey()
    pub = key.publickey().exportKey()

    print(priv)
    fd = open(privKeyName, 'wb')
    fd.write(priv)
    fd.close()

    print(pub)
    fd = open(pubKeyName, 'wb')
    fd.write(pub)
    fd.close()


def encrypt(text, key):
    key = RSA.importKey(key)
    encrypted = key.encrypt(text, 3422)
    print(encrypted)
    return encrypted


def decrypt(text, key):
    key = RSA.importKey(key)
    decrypted = key.decrypt(text)
    print(decrypted)
    return decrypted