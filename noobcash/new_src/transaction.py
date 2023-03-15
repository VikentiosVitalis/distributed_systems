from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import Crypto
from Crypto.Hash import SHA256



class Transaction:
    def __init__(self, sender, receiver, ammount, tid=None, signature=None, transactionInputs=None, transactionOutputs=None):
        self.receiver = receiver  # Address of receiver
        self.sender = sender  # Address of sender
        self.ammount = ammount
        if tid != None:
            self.tid = tid
        else:
            self.tid = Crypto.Random.get_random_bytes(128)
        self.signature = signature
        self.transactionInputs = transactionInputs
        self.transactionOutputs = transactionOutputs

    # Checks if transaction is valid
    def verifySignature(self):
        if self.signature == None:
            return False
        # Load tid to SHA256
        tmp = SHA256.new()
        tmp.update(self.tid)
        # Cipher for verification
        cipher = PKCS1_v1_5.new(RSA.import_key(self.sender))
        # Verify
        return cipher.verify(tmp, self.signature)
