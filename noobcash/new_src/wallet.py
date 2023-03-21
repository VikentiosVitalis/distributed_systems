from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from new_src.transaction import Transaction
from new_src.transactions_output import TransactionOutput
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
        self.balance = 100*int(nodeNr)
        self.prevOutput = 0
        self.unspentOutputs = []

    def get_addr(self):
        return self.publicKey
    
    def sign(self, message):
        # Sign message = sign message
        tmp = SHA256.new()
        tmp.update(message)
        signer = PKCS1_v1_5.new(RSA.import_key(self._privateKey)) 
        ciphertext = signer.sign(tmp)
        return ciphertext
    
    def getMyBalance(self):
        return self.balance

    def getBalance(self, address):
        for tr in self.transactions:
            if tr.sender == address:
                sum = sum - tr.ammount
            if tr.receiver == address:
                sum = sum + tr.ammount
        return sum

    def getMoney(self, amount):
        if amount > self.balance:
            print("Not enough coins!")
            return []
        tmp = 0
        transactions = []
        while tmp < amount:
            tr = self.unspentOutputs.pop(0)
            transactions.append(tr.tid)
            tmp += tr.amount
            tr.unspent = False
        self.balance -= tmp
        print(self.balance)
        return transactions, tmp

    def addTransaction(self, transaction):
        # If this wallet is in the transaction add the money to my list
        if transaction.sender == self.publicKey and transaction.outputSender.amount > 0:
            self.unspentOutputs.append(transaction.outputSender)
            self.balance += transaction.outputSender.amount
        if transaction.receiver == self.publicKey and transaction.outputReceiver.amount > 0:
            self.unspentOutputs.append(transaction.outputReceiver)
            self.balance += transaction.outputReceiver.amount
        # Add to transaction list
        self.transactions.append(transaction)
        print(self.balance)
        return


