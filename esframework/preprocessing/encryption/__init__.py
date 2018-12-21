""" File for Codec simular like tooling """
import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from esframework.exceptions import EncryptionCodecError


class EncryptingCodec(object):

    def __init__(self, encryption_key=None, iv=None):
        if encryption_key is None:
            raise EncryptionCodecError("Missing encryption key")

        if len(encryption_key) != 32:
            raise EncryptionCodecError(
                "Encryption key does not have the correct length of 32 characters.")

        self.__encoding = 'utf-8'
        encryption_key = encryption_key.encode(self.__encoding)

        self.__encryption_key = SHA256.new(encryption_key).digest()
        self.__iv = Random.new().read(AES.block_size)

        if iv is not None:
            self.__iv = iv

    def encrypt(self, plain_text, encode=True):
        plain_text = plain_text.encode(self.__encoding)
        encryptor = AES.new(self.__encryption_key, AES.MODE_CBC, self.__iv)
        padding = AES.block_size - len(plain_text) % AES.block_size  # calculate needed padding
        plain_text += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
        data = self.__iv + encryptor.encrypt(plain_text)  # store the IV at the beginning and encrypt
        return base64.b64encode(data).decode(self.__encoding) if encode else data

    def decrypt(self, encrypted_text, decode=True):
        if decode:
            encrypted_text = base64.b64decode(encrypted_text.encode(self.__encoding))
        IV = encrypted_text[:AES.block_size]  # extract the IV from the beginning

        decryptor = AES.new(self.__encryption_key, AES.MODE_CBC, IV)
        data = decryptor.decrypt(encrypted_text[AES.block_size:])  # decrypt
        padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
        if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
            raise ValueError("Invalid padding...")
        return data[:-padding].decode(self.__encoding)
