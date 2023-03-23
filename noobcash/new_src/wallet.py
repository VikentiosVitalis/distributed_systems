from Crypto import PublicKey
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from new_src.transaction import Transaction
from new_src.transactions_output import TransactionOutput

# Wallet:
#   A wallet is associated with a public/private key pair. 
#
#   The public key acts as an address of the wallet, which a process/user can share with anyone in order to get NBCs. 
#
#   The private key is used to sign transactions. With its use it is ensured that only the wallet owner can spend    #   NBCs from the specific wallet. The sign_transaction function implements this functionality.
# 
#   Anyone who knows the public key of a wallet can verify that a transaction was created by its owner.

class Wallet:
    def __init__(self):
        # Generate key
        key = RSA.generate(1024)
        # Get data from keys
        self._privateKey = key.exportKey()
        # Also user's address
        self.publicKey = key.publickey().exportKey().decode('ISO-8859-1')
        # Transaction list
        self.transactions = []
        self.tr_dict = {} # tid : transaction index in transactions
        self.balances = {}
        self.balances[self.publicKey] = 0
        self.prevOutput = 0
        self.unspentOutputs = []

    def get_addr(self):
        return self.publicKey
    
    def sign(self, message):
        # Sign message = sign message
        tmp = SHA256.new()
        tmp.update(message.encode('ISO-8859-1'))
        signer = PKCS1_v1_5.new(RSA.import_key(self._privateKey)) 
        ciphertext = signer.sign(tmp)
        return ciphertext
    
    def getMyBalance(self):
        return self.balances[self.publicKey]

    def getBalance(self, address):
        return self.balances[address]

    def getMoney(self, amount):
        if amount > self.getMyBalance():
            print("Not enough coins! ", self.getMyBalance())
            return []
        tmp = 0
        transactions = []
        while tmp < amount:
            tr = self.unspentOutputs.pop(0)
            transactions.append(tr.tid)
            tmp += tr.amount
        return transactions, tmp
    
    def setOutputs(self, ipList):
        for tup in ipList:
            self.balances[tup[2]] = 0

    def addTransaction(self, transaction):
        if transaction.tid in self.tr_dict: 
            return # No duplicates

        for tid in transaction.inputs.previous_output_id:
            w = self.tr_dict[tid]
            tr = self.transactions[w]
            if tr.sender == transaction.sender:
                if tr.outputSender.unspent == False:
                    print("Transaction already used:", tr.tid)    
                tr.outputSender.unspent = False
            else:
                if tr.outputReceiver.unspent == False:
                    print("Transaction already used:", tr.tid)
                tr.outputReceiver.unspent = False

        # If this wallet is in the transaction add the money to my list
        if transaction.sender == self.publicKey and transaction.outputSender.amount > 0:
            self.unspentOutputs.append(transaction.outputSender)
        if transaction.receiver == self.publicKey and transaction.outputReceiver.amount > 0:
            self.unspentOutputs.append(transaction.outputReceiver)
        
        self.balances[transaction.receiver] += transaction.outputReceiver.amount
        # Only false for bootstrap
        if transaction.sender != transaction.receiver:
            self.balances[transaction.sender] -= transaction.outputReceiver.amount

        # Add to transaction list
        self.transactions.append(transaction)
        self.tr_dict[transaction.tid] = len(self.transactions) - 1

        print('Current balance:', self.getMyBalance())
        return


