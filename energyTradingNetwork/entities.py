import rsa

class House:
    def __init__(self, productionRate, consumptionRate, batteryHolding, address, balance):
        self.productionRate = productionRate
        self.consumptionRate = consumptionRate
        self.batteryHolding = batteryHolding
        self.address = address
        self.balance = balance


class PowerPlant:
    def __init__(self, productionRate):
        self.productionRate = productionRate

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fees = 0

class Block:
    def __init__(self, prevKey):
        self.listOfTransactions = []
        self.prevKey = prevKey
        self.curKey = ""
        self.next = None

    def pushT(self, sender, receiver, amount):
        tx = Transaction(sender, receiver, amount)
        self.listOfTransactions.append(tx)

    def validate(self):
        # return True or False
        
        pass

    def encrypt(self):
        # return encryptionKey
        txString = ""
        txString += self.prevKey
        for tx in self.listOfTransactions:
            txString += tx.sender + tx.receiver + str(tx.amount) + str(tx.fees)
        pubkey, privkey = rsa.newkeys(1000)
        encString = rsa.encrypt(txString.encode(), pubkey)

        tempRes = 0
        for i in range(len(encString)):
            tempRes += encString[i]*i
        self.curKey = str(tempRes)
        return self.curKey


# class BlockChain:
#     def __init__(self, head):
#         GenesysBlock = Block()
#         self.head = GenesysBlock
#     def pushB(Block b):
#         if (b.validate() == True):
#             key = 