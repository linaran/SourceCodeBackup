import pickle
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


# noinspection PyMethodMayBeStatic
class DigitalSignature(object):
    def __init__(self, rsa_key):
        self.rsa_key = rsa_key

    def public_key(self):
        return self.rsa_key.publickey()

    def digest(self, message):
        return SHA256.new(message).hexdigest()

    def encrypt_digest(self, digest):
        cipherdigest = self.rsa_key.decrypt(digest)
        return cipherdigest

    def create_signature(self, message, output_address=None):
        digest = self.digest(message)
        cipherdigest = self.encrypt_digest(digest)

        if output_address:
            pickle.dump((message, cipherdigest), open(output_address, 'wb'))

        return message, cipherdigest

    def verify_signature(self, signature, sender_public_key, stdout=False):
        message, cipherdigest = signature
        digest = sender_public_key.encrypt(cipherdigest, 32)
        received_digest = self.digest(message)
        ret_value = message if digest[0] == received_digest else None

        if stdout:
            print "Signature -------------\n", ret_value, "\n------------- Signature"

        return ret_value

    def verify_signature_from_disk(self, input_address, sender_public_key, stdout=False):
        signature = pickle.load(open(input_address, 'rb'))
        return self.verify_signature(signature, sender_public_key, stdout)

# user_a = DigitalSignature(RSA.generate(2048))
# user_b = DigitalSignature(RSA.generate(2048))
# digital_signature_a = user_a.create_signature("The answer is no", './signature')
# # user_b.verify_signature(digital_signature_a, user_a.public_key(), True)
# user_b.verify_signature_from_disk('./signature', user_a.public_key(), True)
