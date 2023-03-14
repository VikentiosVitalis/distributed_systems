from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import Crypto
from Crypto.Hash import SHA256



class Transaction:
    def __init__(self, sender, receiver, ammount):
        self.receiver = receiver  # Address of receiver
        self.sender = sender  # Address of sender
        self.ammount = ammount
        self.tid = Crypto.Random.get_random_bytes(128)
        self.signature = None

    # Checks if transaction is valid
    def validTransaction(self):
        if self.signature == None:
            return False
        tmp = SHA256.new()
        tmp.update(self.tid)
        
        cipher = PKCS1_v1_5.new(RSA.import_key(self.sender))
        
        return cipher.verify(tmp, self.signature)
