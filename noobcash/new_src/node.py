from wallet import Wallet
from transaction import Transaction
import requests
import json

class Node: 
    def __init__(self, port, IP, nodeNr, bootstrap):
        self.wallet = Wallet()
        self.port = port
        self.IP = IP
        self.nodeNr = nodeNr
        self.fullAddr = "http://" + self.IP + ":" + str(self.port)
        self.bootstrap = (bootstrap.lower() == 'true')              # Boolean
        self.wallet = Wallet()
        self.ipList = [(0, self.fullAddr, self.wallet.get_addr())]
        self.id = 0
        self.nodesActive = 0
        
        if not self.bootstrap:
            print("child joining")
            res = {'addrr': "http://" + self.IP + ":" + str(self.port), 'pub_key': self.wallet.get_addr()}
            res = json.dumps(res)
            requests.post(self.ring[0] + "/bootstrap_register", data=res, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

        

    def addNode(self, IP, addr):
        # If not bootstrap node return False
        if self.bootstrap == False:
            return False
        self.ipList.append((self.nodesActive+1, IP, addr))
        self.nodesActive += 1
        # Transact 100*n NBC coins
        if self.nodesActive == self.nodeNr:
            broadcast(Node)
        
        

    def createTransaction(self, receiver, ammount):
        print("Creating transaction.")
        # Create transaction
        new_transaction = Transaction(self.get_addr(), receiver, ammount)
        # Sign it
        new_transaction.signature = self.wallet.sign(new_transaction.tid)
        # Broadcast it
        self.broadcast(new_transaction)
        # Add to wallet
        self.wallet.addTransaction(new_transaction)


    def broadcast(transaction):
        # Broadcast Transaction to everyone
        return 

    def validateTransaction(self, transaction):
        # Check signature
        if not transaction.verifySignature():
            return 'Signature verification failed'
        if transaction.sender == transaction.receiver: 
            return 'Sending yourself money is forbidden.'
        # Keep going here... 

        # Check mone
        amt = self.wallet.getBalance(transaction.sender)
        return amt >= transaction.ammount


