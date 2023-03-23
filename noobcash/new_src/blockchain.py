from new_src.block import Block
import new_src.node as node
import time
import requests
import threading
# Noobcash Blockchain:
#  The list of blocks which are verified

class Blockchain:
    def __init__(self, maxTransactions=2):
        self.maxTransactions = maxTransactions # Max transactions in block
        self.blockchain = []
        self.transactions = []                 # Storage of transactions till 
        self.stopMine = threading.Event()

    def genBlock(self):
        return self.blockchain[0]

    def addBlock(self, block):
        self.blockchain.append(block)

    def getLastHash(self):
        return self.blockchain[-1].current_hash

    def convert_chain(self):
        res = []
        for bl in self.blockchain:
            res.append(bl.convert_block())
        return res

    def insert(self, transaction, ipList, id):
        self.transactions.append(transaction)
        if len(self.transactions) == self.maxTransactions:
            node.minings.set()
            newBlock = Block(len(self.blockchain), self.transactions, 0, self.blockchain[-1].current_hash)
            self.transactions = []
            self.stopMine.clear()
            mine = threading.Thread(name='mine', target=self.mine, args=(newBlock,ipList,id,))
            mine.start()

    def mine(self, newBlock, ipList, id):
        print('Starting to mine.')
        begin = time.time()
        newBlock.mine_block(self.stopMine)
        if not self.stopMine.isSet():
            node.bcLock.acquire()
            self.blockchain.append(newBlock)
            node.bcLock.release()
            #fd = open('times/mining' + '.txt', 'a')
            #fd.write(str(time.time() - float(begin)) + '\n')
            #fd.close()
            print('Time taken:', time.time()-begin)
            node.minings.clear()
            self.broadcastBlock(newBlock, time.time(), ipList, id)
        else:
            print('Stopped mine.')

    def broadcastBlock(self, block, startTime, ipList, id):
        print('Broadcasting Block.')
        tmp = {'lb': block.convert_block(), 'mt': startTime}
        for ip in ipList:
            if ip[0] !=  id:
                requests.post(ip[1] + "/mine", json=tmp, headers={
                              'Content-type': 'application/json', 'Accept': 'text/plain'})
        return


