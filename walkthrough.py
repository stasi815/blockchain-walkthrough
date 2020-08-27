import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = [] #empty list that we'll add blocks too; our blockchain
        self.pending_transactions = [] #used for when users send our "coins" to each other until we add them to a new block

        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.", proof=100) #call to self.new_block; represents original Genesis block; proof=100 complex proof of work

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block listing key/value pairs of block information in a JSON object.
        Reset the list of pending transactions & append the newest block to the chain.
        """
        #new block definition; comprised of key-value pairs (dictionary)
        block = {
            #take the length of our blockchain and add 1 to it; indexes start at 1 index
            'index': len(self.chain) + 1,
            #Stamp the block when it's created
            'timestamp': time(),
            #sitting in pending list at initialization of chain;Transactions that are sitting in the ‘pending’ list will be included in our new block
            'transactions': self.pending_transactions,
            # A proof is a random number which is very difficult to find unless you have dedicated high-performance machines running around-the-clock.
            'proof': proof,
            #hashed version of most recent approved block
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block

#Search the blockchain for the most recent block.

    @property
    def last_block(self):
        """
        Search the blockchain for the most recent block.
        """
        #goes to last one in the list
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        """
        Add a transaction with relevant info to the 'blockpool' - list of pending tx's.
        """
        #yet to be verified or blocked; hasn't been added to chain yet
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        # Return the index of the block to which our new transaction will be added.
        #hasn't been added yet, will be added to the next block; return the
        #index of the block to which our new transaction will be added; we want
        #to know where the transaction was created; which block it was created in/inserted
        return self.last_block['index'] + 1

    def hash(self, block):
        """
        Receive one block.
        Turn it into a string, turn that into Unicode (for hashing).
        Hash with SHA256 encryption, then translate the Unicode into a hexidecimal string.
        """
        #cryptography part of blockchain; every block has record of previous
        #hash; each hash changes each previous hash;hash code facilitates
        #enforcing tamper proof aspect of the blockchain

        #take block(dict) and turn into str
        string_object = json.dumps(block, sort_keys=True)

        #convert string into bytes for the hash function
        block_string = string_object.encode()
        #secure hash algorithm (sha)
        raw_hash = hashlib.sha256(block_string)

        #Return the encoded data in hexadecimal format
        hex_hash = raw_hash.hexdigest()

        return hex_hash


blockchain = Blockchain()
t1 = blockchain.new_transaction("Satoshi", "Mike", '5 BTC')
t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
t3 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
blockchain.new_block(12345)

t4 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
t5 = blockchain.new_transaction("Alice", "Bob", '0.5 BTC')
t6 = blockchain.new_transaction("Bob", "Mike", '0.5 BTC')
blockchain.new_block(6789)

print("Genesis block: ", blockchain.chain)