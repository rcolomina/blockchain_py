#!/usr/bin/python3

# 1. Import dependencies

# generate timestamps
import datetime

# contains hashing algorithms
import hashlib

# 2. Create a block
# Message myfile.txt  --> Hash Algorithm (sha256) --> Hash Value

# defining the block data structure

class Block:
    # each block has 7 attributes
    # 1 number of the block
    # 2 what data is sotred in this block?
    # 3 pointer to the next block
    # 4 the hash of this block (serves as a unique ID and verifies its integrity)
    # 5 a nonce is a number only used once
    # 6 store the hash (ID) of the previous block in the chain
    # 7 timestamp
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.datetime.now()
    
    # We initialize a block by storing some data in it
    def __init__(self,data):
        self.data = data
    
    # Function to compute 'hash' of a block
    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8')+
            str(self.data).encode('utf-8')+
            str(self.previous_hash).encode('utf-8')+
            str(self.timestamp).encode('utf-8')+
            str(self.blockNo).encode('utf-8'))

        return h.hexdigest()

    def __str__(self):
        # print out the value of a block
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + \
            "\nBlock Data: "+ str(self.data) + "\nNonce: " + str(self.nonce) + "\n------------"
    

# 3 Create a blockchain

# define the blockchain datastructure
# consists of 'blocks' linked together

class Blockchain:

    maxNonce = 2**32
    diff = 15
    target = 2 ** (256-diff)
    
    # generate the first block in the blockchain
    block = Block("Genesis")
    # set it as the head of our blockchain
    head = block
    
    # adds a given block to the chain of blocks
    def add(self, block):
        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next


    # determines whether or not we can add a given block to the blockchain
    #
    # Bitcoin's Proof-of-Work
    # Find a nonce x such that SHA-256(SHA-256(r||x)) < T/d
    #
    def mine(self, block):
        print("Start mining block")
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                #print(block)
                break
            else:
                block.nonce += 1
        print("Found solution with nonce " + str(block.nonce) + \
              "\nHash found:"+str(int(block.hash(), 16)))

# 4 Print the blockchain
blockchain = Blockchain()

print("Blockchain target difficulty: \n"+ str(blockchain.target))

# mine 10 blocks
for n in range(10):
    blockchain.mine(Block("Here is your data block - block number = " + str(n + 1)))

# print out each block in the blockchain
while blockchain.head != None:
    print(blockchain.head)
    blockchain.head = blockchain.head.next
    
