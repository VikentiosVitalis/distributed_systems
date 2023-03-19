from new_src.wallet import Wallet
from new_src.transaction import Transaction
from new_src.blockchain import Blockchain
import time
import requests
import json
import threading


class Node:
    def __init__(self, port, IP, nodeNr, bootstrap):
        self.port = port
        self.IP = IP
        self.addr = "http://" + self.IP + ":" + str(self.port)

        # Assuming bootstrap's always there
        self.bootstrapAddr = 'http://192.168.0.3:5000'
        self.bootstrap = (bootstrap.lower() == 'true')              # Boolean

        self.nodeNr = int(nodeNr)
        self.wallet = Wallet(nodeNr)
        self.ipList = [(0, self.bootstrapAddr, self.wallet.get_addr())]
        self.id = 0
        self.nodesActive = 0
        self.buffer = []


        self.mining = threading.Event()  # Switch between mining
        self.mining.clear()              # No mining at the start

        # Flag that indicates that we have all nodes
        self.nodeFlag = threading.Event()
        self.nodeFlag.clear()
            
        
        waitThread = threading.Thread(target=self.waitThread)
        waitThread.start()


        if self.bootstrap:
            bootThread = threading.Thread(target=self.broadcastNodes)
            bootThread.start()
        else:
            res = {'addrr': self.addr, 'pub_key': self.wallet.get_addr()}
            res = json.dumps(res)
            requests.post(self.bootstrapAddr + "/bootstrap_register", data=res,
                          headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

    def addNode(self, IP, addr):
        self.ipList.append((self.nodesActive + 1, IP, addr))
        self.nodesActive += 1
        if self.nodesActive >= self.nodeNr:
            self.nodeFlag.set()
        return True

    def setIPList(self, ipList):
        self.ipList = ipList
        self.id = self.getID(self.wallet.get_addr())
        print('My id:', self.id)
        return

    def getBalance(self):
        return self.wallet.getMyBalance()

    def getAddr(self, id):
        return self.ipList[id][2]

    def getID(self, addr):
        for i in self.ipList:
            if i[2] == addr:
                return i[0]
        print('Error: Not existant address.')
        return self.ipList[0][2]

    def createTransaction(self, receiverID, ammount):
        print("Creating transaction.")
        now = time.time()
        # Create transaction
        new_transaction = Transaction(self.wallet.get_addr(), self.getAddr(receiverID), ammount)
        # Sign it
        new_transaction.signature = self.wallet.sign(new_transaction.tid)
        self.broadcastTransaction(new_transaction)
        now = time.time() - now
        #fd = open('times/transactions_t' + str(self.id) +  '.txt', 'a')
        #fd.write(str(now) + ' \n')
        #fd.close()
        return new_transaction

    def waitThread(self):
        self.nodeFlag.wait()
        return

    def broadcastNodes(self):
        self.nodeFlag.wait()
        print('Sharing children IDs')
        # Broadcast Nodes to everyone
        ipList = {
            'ipList': self.ipList
        }
        ipList = json.dumps(ipList)
        print('IP list:', ipList)
        for tup in self.ipList[1:]:
            requests.post(tup[1]+'/child_inform', data=ipList,
                          headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

    def broadcastTransaction(self, transaction):
        # Broadcast Transaction to everyone
        print("Broadcasting Transaction: ", transaction.tid)
        tmp = json.loads(transaction.toJSON())
        print(tmp)
        for ip in self.ipList:
            if ip[0] != self.id:
                requests.post(ip[1] + "/broadcast", json=tmp, headers={
                              'Content-type': 'application/json', 'Accept': 'text/plain'})
        return

    def validateTransaction(self, transaction):
        # Check signature
        if not transaction.verifySignature():
            return 'Signature verification failed.'
        if transaction.sender == transaction.receiver:
            return 'Sending yourself money is forbidden.'
        # Check money
        amt = self.wallet.getBalance(transaction.sender)
        if amt < transaction.amount: 
            return 'Account balance too low.'
        if amt < 0: 
            return 'Negative Coins.'
        return 'Accepted.'

    def resolveConflict(self):
        # Resolve some conflict
        return
