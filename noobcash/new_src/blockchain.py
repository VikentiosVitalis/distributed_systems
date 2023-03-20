from new_src.block import Block

# Noobcash Blockchain:
#  The list of blocks which are verified

class Blockchain:
    def __init__(self):
        self.blockchain = []

    def addBlock(self, block):
        self.blockchain.append(block)
