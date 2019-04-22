import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from base64 import b64decode

backend = default_backend()

def enc(passwd, ivval, salt, blocksize):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=blocksize, #length in bytes
        salt=salt,
        iterations=100000, #min is 100,000
        backend=backend
        )
    key = kdf.derive(passwd)    #(bytes(passwd, "utf8"))
    
    idf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=blocksize,
        salt=salt,
        iterations=100000,
        backend=backend
        )
    iv = idf.derive(ivval)  #(bytes(ivval, "utf8"))       #use same key&ivval as task72?
    
    cipher = Cipher(
        algorithm=algorithms.AES(key), 
        mode=modes.CBC(iv),
        backend=backend
        )
    
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()

    #path = os.path.abspath(fnameData)
    #path2 = os.path.abspath(fnameDataEnc)

    #blocksize=16
    #mydata = bytearray(blocksize)
    
    #open the files
    #file = open(fnameData, "rb")
    #file2 = open(fnameDataEnc, "wb")
    
    #initialize vars for loop
    #totalsize = 16
    #data = padder.update(salt)
    #file2.write(bytearray(data))
    return key, encryptor, padder, iv
    
def encFile(mydata, encryptor, padder, salt):
    #data = padder.update(salt)
    #while True:
    #read block from source file
    num = len(mydata)    #is it working with bytearray or still trying for strinig?
    #encryptor = cipher.encryptor()
    #try:
        #if num == blocksize:    #*2:
            #data = padder.update(bytes(mydata))
            #ciphertext = encryptor.update(data)
    data = padder.update(bytes(mydata, "utf-8")) + padder.finalize()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    dataEnc = bytes(ciphertext)#bytearray(ciphertext)
    #except ValueError:
    #    print("data is incorrect size")
        #mydata2 = mydata[0:num]
        #data = padder.update(bytes(mydata)) + padder.finalize()
        #ciphertext = encryptor.update(data) + encryptor.finalize()
        #file2.write(bytearray(ciphertext))
#        break
        
    
    print('encrypting read ', num, ' bytes')
    #file.close()
    #file2.close()
    #print("dataenc ", dataEnc)
    #print("bytarray ", bytearray(ciphertext))
    #print("mydata ", mydata)
    print("data ", data)
    print("ciphertext ", ciphertext)
    return dataEnc

def decFile(mydata, blocksize, iv, key):
    #blocksize=16
    #mydata = bytearray(blocksize)
    
    #file = open(fnameDataEnc, "rb")
    #file2 = open(fnameDataDec, "wb")
    
    #totalsize = 16

    #salt = bytearray(blocksize)
    #file.readinto(salt)
    #salt = mydata[:16]
    '''
    idf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=blocksize,
        salt=salt,
        iterations=100000,
        backend=backend
        )
    iv = idf.derive(bytes(ivval, "utf8"))
    '''
    cipher = Cipher(
        algorithm=algorithms.AES(key), 
        mode=modes.CBC(iv),
        backend=backend
        )
       
    unpadder = padding.PKCS7(128).unpadder()
    decryptor = cipher.decryptor()
    #pdata = unpadder.update(bytes(salt))
    
    #path = os.path.abspath(fnameDataEnc)
    #path2 = os.path.abspath(fnameDataDec)
    
    #filesize = os.path.getsize(path)

    #while True:
    num = len(mydata)
    print(num)
    print("block\n", unpadder.block_size)
    print("buffer\n", len(unpadder._buffer))
        #totalsize += num

    #    try:
    #        if num == blocksize: #num == blocksize:
                #plaintext = decryptor.update(bytes(mydata))
                #data = unpadder.update(plaintext)
    plaintext = decryptor.update(mydata) + decryptor.finalize()
    # plaintext = decryptor.update(bytes(mydata)) + decryptor.finalize()
    print(len(plaintext))
    print("Plaintext",plaintext)
    data = unpadder.update(plaintext)+ unpadder.finalize()
    #print("Length",len(unpadder._buffer))
    print ("data", data)
    #data += unpadder.finalize()
    dataDec = data
                #file2.write(data)
    #    except ValueError:
    #        print("data is incorrect size")
            #plaintext = decryptor.update(bytes(mydata)) + decryptor.finalize()
            #data = unpadder.update(plaintext) + unpadder.finalize()
    #        break
        
    #file.close()
    #file2.close()
    return dataDec

"""
def encFile(mydata, blocksize, passwd, ivval, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=blocksize, #length in bytes
        salt=salt,
        iterations=100000, #min is 100,000
        backend=backend
        )
    key = kdf.derive(passwd)    #(bytes(passwd, "utf8"))

    idf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=blocksize,
        salt=salt,
        iterations=100000,
        backend=backend
        )
    iv = idf.derive(ivval)  #(bytes(ivval, "utf8"))       #use same key&ivval as task72?
    
    cipher = Cipher(
        algorithm=algorithms.AES(key), 
        mode=modes.CBC(iv),
        backend=backend
        )
    
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()

    #path = os.path.abspath(fnameData)
    #path2 = os.path.abspath(fnameDataEnc)

    #blocksize=16
    #mydata = bytearray(blocksize)
    
    #open the files
    #file = open(fnameData, "rb")
    #file2 = open(fnameDataEnc, "wb")
    
    #initialize vars for loop
    #totalsize = 16
    data = padder.update(salt)
    #file2.write(bytearray(data))
    
    #while True:
    #read block from source file
    num = len(mydata)    #is it working with bytearray or still trying for strinig?

    #try:
        #if num == blocksize:    #*2:
            #data = padder.update(bytes(mydata))
            #ciphertext = encryptor.update(data)
    data = padder.update(bytes(mydata, "utf8")) + padder.finalize()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    dataEnc = bytearray(ciphertext)
    #except ValueError:
    #    print("data is incorrect size")
        #mydata2 = mydata[0:num]
        #data = padder.update(bytes(mydata)) + padder.finalize()
        #ciphertext = encryptor.update(data) + encryptor.finalize()
        #file2.write(bytearray(ciphertext))
#        break
        
    
    print('encrypting read ', num, ' bytes')
    #file.close()
    #file2.close()
    return key, dataEnc
    """