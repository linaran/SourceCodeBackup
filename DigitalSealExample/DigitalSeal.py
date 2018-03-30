from DigitalEnvelope import DigitalEnvelope
from DigitalSignature import DigitalSignature
from Crypto.PublicKey import RSA
import pickle


# noinspection PyMethodMayBeStatic
class DigitalSeal(object):
    def __init__(self, rsa_key):
        self.rsa_key = rsa_key

    def public_key(self):
        return self.rsa_key.publickey()

    def make_envelope(self, message, recipient_public_key, output_address):
        return DigitalEnvelope(self.rsa_key).create_envelope(message, recipient_public_key, output_address)

    def sign_envelope(self, envelope_address, output_address):
        file_handler = open(envelope_address, 'r')
        envelope = file_handler.read()
        file_handler.close()
        return DigitalSignature(self.rsa_key).create_signature(envelope, output_address)

    def generate_seal(self, message, recipient_public_key, envelope_address="./envelope",
                      signature_address="./signature"):
        self.make_envelope(message, recipient_public_key, envelope_address)
        return self.sign_envelope(envelope_address, signature_address)

    def verify_signature(self, signature_address, sender_public_key):
        return DigitalSignature(self.rsa_key).verify_signature_from_disk(signature_address, sender_public_key)

    def read_envelope(self, envelope, stdout=False):
        return DigitalEnvelope(self.rsa_key).read_envelope(envelope, stdout)

    def read_seal(self, sender_public_key, signature_address="./signature", stdout=False):
        envelope_str = self.verify_signature(signature_address, sender_public_key)
        if envelope_str is None:
            print "Signature was tempered with; Shutting down;"

        envelope = pickle.loads(envelope_str)
        message = self.read_envelope(envelope, stdout)
        return message


user_a = DigitalSeal(RSA.generate(2048))
user_b = DigitalSeal(RSA.generate(2048))
user_a.generate_seal("The answer is no", user_b.public_key())
user_b.read_seal(user_a.public_key(), stdout=True)
