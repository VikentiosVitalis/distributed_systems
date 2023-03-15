from wallet import Wallet
from transaction import Transaction

class Node: 
    def __init__(self):
        self.id = 0
        self.wallet = Wallet()

    def createTransaction(self, receiver, ammount):
        print("Creating transaction.")
        new_transaction = Transaction(self.get_addr(), receiver, ammount)
        new_transaction.signature = self.wallet.sign(new_transaction.tid)
        self.broadcast(new_transaction)
        self.wallet.addTransaction(new_transaction)


    def broadcast(transaction):
        # Broadcast Transaction to everyone
        return 

    def validateTransaction(self, transaction):
        # Check signature
        if not transaction.validTransaction():
            return False
        # Check money
        amt = self.wallet.getBalance(transaction.sender)
        return amt >= transaction.ammount


