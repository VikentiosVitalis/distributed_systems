from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from new_src.transaction import Transaction

class Wallet:
    def __init__(self, nodeNr):
        # Generate key
        key = RSA.generate(1024)
        # Get data from keys
        self._privateKey = key.exportKey()
        # Also user's address
        self.publicKey = key.publickey().exportKey().decode('ISO-8859-1')
        # Transaction list
        self.transactions = []
        self.balance = 100*nodeNr

    def get_addr(self):
        return self.publicKey
    
    def sign(self, message):
        # Sign message = sign message
        tmp = SHA256.new()
        tmp.update(message)
        signer = PKCS1_v1_5.new(RSA.import_key(self._privateKey.encode('ISO-8859-1'))) 
        ciphertext = signer.sign(tmp)
        return ciphertext
    
    def getBalance(self):
        return self.balance

    def getBalance(self, address):
        sum = 100
        for tr in self.transactions:
            if tr.sender == address:
                sum = sum - tr.ammount
            if tr.receiver == address:
                sum = sum + tr.ammount
        return sum

    def addTransaction(self, transaction):
        self.transactions.append(transaction)
        return


