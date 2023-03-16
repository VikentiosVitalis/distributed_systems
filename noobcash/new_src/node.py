from wallet import Wallet
from transaction import Transaction
import requests
import json
import threading

mining = threading.Event()  # Switch between mining
mining.clear()              # No mining at the start

class Node: 
    def __init__(self, port, IP, nodeNr, bootstrap):
        self.port = port
        self.IP = IP
        self.addr = "http://" + self.IP + ":" + str(self.port)  
        
        self.bootstrapAddr = 'http://192.168.0.3:5000'              # Assuming bootstrap's always there
        self.bootstrap = (bootstrap.lower() == 'true')              # Boolean

        self.nodeNr = nodeNr
        self.wallet = Wallet(nodeNr)
        self.ipList = [(0, self.bootstrapAddr, self.wallet.get_addr())]
        self.id = 0
        self.nodesActive = 0

        waitThread = threading.Thread(target=self.waitThread)
        waitThread.start()

        self.childFlag = threading.Event()      # Flag that indicates that we have all nodes
        self.childFlag.clear()
        print(self.childFlag.isSet())
        
        self.buffer = []

        # Register new node
        if not self.bootstrap:
            print("child joining")
            res = {'addrr': self.addr, 'pub_key': self.wallet.get_addr()}
            res = json.dumps(res)
            requests.post(self.bootstrapAddr + "/bootstrap_register", data=res, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})


    def addNode(self, IP, addr):
        self.ipList.append((self.nodesActive+1, IP, addr))
        self.nodesActive += 1
        if self.nodesActive == self.nodeNr:
            self.childFlag.set()
        return True
    
    def setIPList(self, ipList):
        print(ipList)
        self.ipList = ipList
        self.childFlag.set()

        return

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


    def waitThread(self):
        # Not enough children
        self.childFlag.wait()
        if self.bootstrap:
            self.broadcastNodes()

        while True:
            # As long as we're mining, wait
            if mining.isSet(): 
                mining.wait()
            if len(self.buffer) > 0 and (not mining.isSet()):
                buffer_itm = self.buffer.pop(0)



    def broadcastNodes(self):
        print('Sharing children IDs')
        # Broadcast Nodes to everyone
        ipList = {
            'ipList': self.ipList
        }
        ipList = json.dumps(ipList)
        print('IP list:', ipList)
        for tup in self.ipList[1:]:
            requests.post(tup[1]+'child_inform', data=ipList,headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        return 

    def broadcastTransaction(self, transaction):
        # Broadcast Transaction to everyone
        print("Broadcasting Transaction: ", transaction.tid)
        tmp = json.loads(transaction.toJSON())
        for ip in self.ipList:
            if ip[1] != self.fullAddr:
                requests.post(ip[1] + "/broadcast", json=tmp,headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
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
        return amt >= transaction.amount

    def resolveConflict(self):
        # Resolve some conflict
        return 
