from new_src.block import Block
from new_src.node import minings
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
        self.stopMine.clear()

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
            minings.set()
            newBlock = Block(len(self.blockchain), self.transactions, 0, self.blockchain[-1].current_hash)
            self.transactions = []
            mine = threading.Thread(name='mine', target=self.mine, args=(newBlock,ipList,id,))
            mine.start()
        return

    def mine(self, newBlock, ipList, id):
        print('Starting to mine.')
        begin = time.time()
        newBlock.mine_block(self.stopMine)
        minings.clear()
        if not self.stopMine.isSet():
            # node.valLock.acquire()
            #if  self.stopMine.isSet():
            #    node.valLock.release()
            #    return
            # node.bcLock.acquire()
            self.blockchain.append(newBlock)
            # node.bcLock.release()
            #node.valLock.release()
            fd = open('distributed_systems-main/noobcash/times/mining' + '.txt', 'a')
            fd.write(str(time.time() - float(begin)) + '\n')
            fd.close()
        elf.broadcastBlock(newBlock, time.time(), ipList, id)
        self.stopMine.clear()

    def broadcastBlock(self, block, startTime, ipList, id):
        print('...................................Broadcasting Block...................................................')
        tmp = {'lb': block.convert_block(), 'mt': startTime}
        for ip in ipList:
            if ip[0] !=  id:
                requests.post(ip[1] + "/mine", json=tmp, headers={
                              'Content-type': 'application/json', 'Accept': 'text/plain'})
        return


