import functions
import entities as e

sender = functions.generateAddress()
receiver = functions.generateAddress()
amount = 5.0

block = e.Block('931137')

block.pushT(sender, receiver, amount)
print(block.encrypt())
# print(block.curKey)