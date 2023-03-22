from new_src.wallet import Wallet
from new_src.transaction import Transaction
from new_src.blockchain import Blockchain
from new_src.block import Block
import time
import requests
import json
import threading

notMining = threading.Event()
notMining.set()

consFlag = threading.Event()
consFlag.set()

class Node:
    def __init__(self, port, IP, nodeNr, bootstrap):
        self.port = port
        self.IP = IP
        self.addr = "http://" + self.IP + ":" + str(self.port)

        # Assuming bootstrap's always there
        self.bootstrapAddr = 'http://192.168.0.3:5000'
        self.bootstrap = (bootstrap.lower() == 'true')              # Boolean
        # Money
        self.nodeNr = int(nodeNr)
        self.wallet = Wallet()
        # For consensus
        self.allBlockchains = {}
        self.currentBlock = None
        # IPs
        self.ipList = [(0, self.bootstrapAddr, self.wallet.get_addr())]
        self.id = 0
        self.nodesActive = 0
        # Buffer to store incoming transactions
        self.buffer = []
        #Blockchain
        self.blockchain = Blockchain()

        # Flag that indicates that we have all nodes
        self.nodeFlag = threading.Event()
        self.nodeFlag.clear()

        waitThread = threading.Thread(target=self.waitThread)
        waitThread.start()

        if self.bootstrap:
            bootThread = threading.Thread(target=self.broadcastNodes)
            bootThread.start()
            tr = Transaction(self.wallet.get_addr(),
                             self.wallet.get_addr(), 100*(self.nodeNr+1), [], 0)
            tr.signature = self.wallet.sign(tr.tid)
            genBlock = Block(0, [tr], 0, 1)
            self.blockchain.addBlock(genBlock)
            self.wallet.addTransaction(tr)

        else:
            res = {'addrr': self.addr, 'pub_key': self.wallet.get_addr()}
            res = json.dumps(res)
            requests.post(self.bootstrapAddr + "/bootstrap_register", data=res,
                          headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

    def addNode(self, IP, addr):
        self.ipList.append((self.nodesActive + 1, IP, addr))
        self.wallet.balances[addr] = 0
        self.nodesActive += 1
        if self.nodesActive >= self.nodeNr:
            self.nodeFlag.set()
        return True

    def setIPList(self, ipList):
        self.ipList = ipList
        self.wallet.setOutputs(self.ipList)
        self.id = self.getID(self.wallet.get_addr())
        print('My id:', self.id)
        return

    def getSK(self):
        return [i[2] for i in self.ipList]

    def setGenesis(self, block):
        genesisblock = json.loads(block)
        # print(genesisblock['transactions'])
        t = json.loads(genesisblock['transactions'][0])    # Load the transaction
        transaction = Transaction(
            t['sender'], t['receiver'], t['amount'], t['inputs'], t['amtLeft'], t['tid'], t['signature'].encode('ISO-8859-1'))
        current_block = Block(
            genesisblock['index'], [transaction], genesisblock['nonce'],
            genesisblock['previous_hash']
        )
        self.blockchain.addBlock(current_block)
        print('Initialized.')
        self.wallet.addTransaction(transaction)
        self.nodeFlag.set()

    def getBalance(self):
        return self.wallet.getMyBalance()

    def getAddr(self, id):
        return self.ipList[id][2]
    
    def getFullAddr(self):
        return self.ipList[self.id][1]
    
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
        prev_tr, amt = self.wallet.getMoney(ammount)
        new_transaction = Transaction(self.wallet.get_addr(), self.getAddr(receiverID), 
                                      ammount, prev_tr, amt-ammount)
        # Sign it
        new_transaction.signature = self.wallet.sign(new_transaction.tid)
        self.broadcastTransaction(new_transaction)
        now = time.time() - now
        print(self.validateTransaction(new_transaction))
        self.wallet.addTransaction(new_transaction)
        # fd = open('times/transactions_t' + str(self.id) +  '.txt', 'a')
        # fd.write(str(now) + ' \n')
        # fd.close()
        return new_transaction

    def waitThread(self):
        self.nodeFlag.wait()
        while True:
            if not notMining.isSet():
                notMining.wait()
            if consFlag.isSet():
                consFlag.wait()
            
            if len(self.buffer) != 0 and notMining.isSet():
                print(f'Reading transaction from', end="")
                itm = self.buffer.pop()
                sender, receiver, amt, inputs, amtLeft, tid, signature = itm
                tr = Transaction(sender, receiver, amt, inputs, amtLeft, tid, signature.encode('ISO-8859-1'))
                print(f" {self.getID(sender)} to {self.getID(receiver)}.")
                # If invalid ignore block
                if self.validateTransaction(tr) != 'Accepted.': 
                    print(self.validateTransaction(tr))
                    continue
                # Insert to block
                self.blockchain.insert(tr, self.ipList, self.id)
                self.wallet.addTransaction(tr)

        
    def broadcastNodes(self):
        self.nodeFlag.wait()
        print('All nodes joined, sharing IDs')
        time.sleep(2)
        # Broadcast Nodes to everyone
        ipList = {
            'ipList': self.ipList,
            'genBlock': self.blockchain.genBlock().convert_block()
        }
        ipList = json.dumps(ipList)
        # print('IP list:', ipList)
        for tup in self.ipList[1:]:
            requests.post(tup[1]+'/child_inform', data=ipList,
                          headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

        time.sleep(2)
        for tup in self.ipList[1:]:
            if notMining.isSet():
                notMining.wait()
            self.createTransaction(tup[0], 100)
        return

    def broadcastTransaction(self, transaction):
        # Broadcast Transaction to everyone
        print("Broadcasting Transaction.")
        tmp = json.loads(transaction.toJSON())
        # print(tmp)
        for tup in self.ipList:
            if tup[0] != self.id:
                requests.post(tup[1] + "/broadcast", json=tmp, headers={
                              'Content-type': 'application/json', 'Accept': 'text/plain'})
        return

    def broadcastConsensus(self):
        print('We\'re consensing!')
        tmp = {'address': self.getFullAddr()}
        for tup in self.ipList:
            if tup[0] != self.id:
                requests.post(tup[1] + "/consensus", json=tmp, headers={
                              'Content-type': 'application/json', 'Accept': 'text/plain'})

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

    def validateBlock(self, block, creationTime):
        self.blockchain.stopMine.set()
        block = json.loads(block)
        newBlock = Block(0,[],0,0)
        newBlock.set(block)
        tmp = newBlock.hashing()
        if tmp != block['current_hash']:
            print('Invalid block with:')
            print(tmp)
            print(block['current_hash'])
            return False
        if consFlag.isSet():
            consFlag.wait()
        consFlag.set()
        if block['previous_hash'] != self.blockchain.getLastHash():
            consFlag.set()
            self.currentBlock = newBlock
            self.broadcastConsensus()
            self.resolveConflict()
            consFlag.clear()
            return True
        self.blockchain.blockchain.append(newBlock)
        consFlag.clear()
        return True

    def resolveConflict(self):
        # Wait for all nodes to send their blockchains
        while len(self.allBlockchains) != self.nodeNr:
            continue
        newChain = max(self.allBlockchains.values(), key=len)
        # Reset dictionary
        self.allBlockchains = {}

        blocks = []
        for newBlock in newChain:
            b = json.loads(newBlock)
            block = Block(0,[],0,0)
            block.set(b)
            blocks.append(block)
        self.blockchain.blockchain = blocks 
        return
