import ecdsa
from time import time

import entities as E
import functions as F


class Block:
    def __init__(self, previous_Key):
        self.listOfTransactions = []
        self.previous_block_Key = previous_Key
        self.current_Key = None
        self.next = None
        self.time_stamp = time()

    def pushT(self, transaction):
        if transaction.validate():
            self.listOfTransactions.append(transaction)

    def get_hash(self):
        self.current_Key = hash(self)
        return self.current_Key

block = Block("XYZ")
print(block.get_hash())
