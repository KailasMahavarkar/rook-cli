import base64
import hashlib
from Cryptodome.Cipher import AES as domeAES
from Cryptodome.Random import get_random_bytes
from Crypto import Random
from Crypto.Cipher import AES as cryptoAES

BLOCK_SIZE = cryptoAES.block_size

class AESCipher():
    def __init__(self, key):
        self.__key__ = hashlib.sha256(key.encode()).digest()
        
    def encrypt(self, raw):
        BS = cryptoAES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        raw = base64.b64encode(pad(raw).encode('utf8'))
        iv = get_random_bytes(cryptoAES.block_size)
        cipher = cryptoAES.new(key= self.__key__, mode= cryptoAES.MODE_CFB,iv= iv)
        a= base64.b64encode(iv + cipher.encrypt(raw))
        IV = Random.new().read(BLOCK_SIZE)
        aes = domeAES.new(self.__key__, domeAES.MODE_CFB, IV)
        b = base64.b64encode(IV + aes.encrypt(a))
        return b

    def decrypt(self, enc):
        passphrase = self.__key__
        encrypted = base64.b64decode(enc)
        IV = encrypted[:BLOCK_SIZE]
        aes = domeAES.new(passphrase, domeAES.MODE_CFB, IV)
        enc = aes.decrypt(encrypted[BLOCK_SIZE:])
        unpad = lambda s: s[:-ord(s[-1:])]
        enc = base64.b64decode(enc)
        iv = enc[:cryptoAES.block_size]
        cipher = cryptoAES.new(self.__key__, cryptoAES.MODE_CFB, iv)
        b=  unpad(base64.b64decode(cipher.decrypt(enc[cryptoAES.block_size:])).decode('utf8'))
        return b
