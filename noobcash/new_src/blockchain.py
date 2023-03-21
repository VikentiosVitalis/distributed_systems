from new_src.block import Block
import new_src.node as node
import time
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

    def insert(self, transaction):
        self.transactions.append(transaction)
        if len(self.transactions) == self.maxTransactions:
            node.notMining.clear()
            newBlock = Block(len(self.blockchain), self.transactions, 0, self.blockchain[-1].current_hash)
            self.transactions = []
            self.stopMine.clear()
            mine = threading.Thread(name='mine', target=self.mine, args=(newBlock,))
            mine.start()

            
    def mine(self, newBlock):
        print('Starting to mine.')
        begin = time.time()
        newBlock.mine_block(self.stopMine)
        if not self.stopMine.isSet():
            self.blockchain.append(newBlock)
            #fd = open('times/mining' + '.txt', 'a')
            #fd.write(str(time.time() - float(begin)) + '\n')
            #fd.close()
            print('Time taken:', time.time()-begin)
            node.broadcast(newBlock, time.time())




        


