import os
import pickle
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


# noinspection PyMethodMayBeStatic
class DigitalEnvelope(object):
    def __init__(self, rsa_key):
        self.rsa_key = rsa_key

    def aes_encrypt(self, message):
        encryption_key = os.urandom(16)
        aes_obj = AES.new(encryption_key, AES.MODE_CBC, 'This is an IV456')
        ciphertext = aes_obj.encrypt(message)
        return ciphertext, encryption_key

    def aes_decrypt(self, ciphertext, encryption_key):
        aes_obj = AES.new(encryption_key, AES.MODE_CBC, 'This is an IV456')
        message = aes_obj.decrypt(ciphertext)
        return message

    def public_key(self):
        return self.rsa_key.publickey()

    def rsa_encrypt(self, message, recipient_public_key):
        # Encryption must be performed with a public key!
        ciphertext = recipient_public_key.encrypt(message, 32)
        return ciphertext

    def rsa_decrypt(self, ciphertext):
        message = self.rsa_key.decrypt(ciphertext)
        return message

    def create_envelope(self, message, recipient_public_key, output_address=None):
        aes_ciphertext, encryption_key = self.aes_encrypt(message)
        crypted_key = self.rsa_encrypt(encryption_key, recipient_public_key)

        if output_address:
            pickle.dump((aes_ciphertext, crypted_key), open(output_address, 'wb'))

        return aes_ciphertext, crypted_key

    def read_envelope(self, envelope, stdout=False):
        # Hooray cheating is impossible.
        aes_ciphertext, crypted_key = envelope
        aes_encryption_key = self.rsa_decrypt(crypted_key)
        message = self.aes_decrypt(aes_ciphertext, aes_encryption_key)

        if stdout:
            print "Message -------------\n", message, "\n------------- Message"
        return message

    def read_envelope_from_disk(self, input_address, stdout=False):
        envelope = pickle.load(open(input_address, 'rb'))
        return self.read_envelope(envelope, stdout)


# user_a = DigitalEnvelope(RSA.generate(2048))
# user_b = DigitalEnvelope(RSA.generate(2048))
# digital_envelope_a = user_a.create_envelope("The answer is no", user_b.public_key(), './envelope')
# # user_b.read_envelope(digital_envelope_a, stdout=True)
# user_b.read_envelope_from_disk('./envelope', stdout=True)
