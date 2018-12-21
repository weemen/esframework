""" Test for encrypting codec """
import unittest

from esframework.exceptions import EncryptionCodecError
from esframework.preprocessing.encryption import EncryptingCodec


class TestEncryptionCodec(unittest.TestCase):
    """ EncryptingCodec tests """

    def setUp(self):
        self.__iv = b'4\xaewY\x13\xb7\xb7\xe6\xbb@\xa1%\xf1I\xbe\xee'
        self.__encryption_key = "5BnzddAoY36fAxnAyQQvJn3Ag5VqPAML"

    def test_it_can_encrypt(self):
        codec = EncryptingCodec(encryption_key=self.__encryption_key, iv=self.__iv)
        self.assertEqual(
            'NK53WRO3t+a7QKEl8Um+7j6Hmd/5ZH7sgtVSYp6gL+g=',
            codec.encrypt("foobarbaz")
        )

    def test_it_must_have_an_encryption_key(self):
        with self.assertRaises(EncryptionCodecError) as ex:
            EncryptingCodec(encryption_key=None, iv=self.__iv)
        self.assertEqual(
            str(ex.exception), "Missing encryption key")

    def test_it_must_have_an_encryption_key_of_32_chars(self):
        with self.assertRaises(EncryptionCodecError) as ex:
            EncryptingCodec(encryption_key="AAAA", iv=self.__iv)
        self.assertEqual(
            str(ex.exception), "Encryption key does not have the correct length of 32 characters.")

    def test_it_can_have_an_random_iv(self):
        codec1 = EncryptingCodec(encryption_key=self.__encryption_key, iv=self.__iv)
        codec2 = EncryptingCodec(encryption_key=self.__encryption_key, iv=None)
        output1 = codec1.encrypt("foobarbaz")
        output2 = codec2.encrypt("foobarbaz")

        self.assertNotEqual(output1, output2)

    def test_it_can_decrypt(self):
        codec = EncryptingCodec(encryption_key=self.__encryption_key, iv=self.__iv)
        self.assertEqual(
            codec.decrypt('NK53WRO3t+a7QKEl8Um+7j6Hmd/5ZH7sgtVSYp6gL+g='),
            'foobarbaz'
        )
