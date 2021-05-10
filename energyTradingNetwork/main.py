import blockchain as B

import functions as F 

def transact(sender_pub_key, receiver_pub_key, sender_priv_key, amount, miner):
    tx = B.Transaction(sender_pub_key, receiver_pub_key, amount)
    tx.sign_transaction(sender_priv_key)
    new_block = B.Block()
    new_block.push_transaction(tx)
    energy_chain.mine(new_block, miner)

# Adding database
F.generate_database()
public_key0, private_key0 = F.generate_keys()
public_key1, private_key1 = F.generate_keys()
public_key2, private_key2 = F.generate_keys()
public_key3, private_key3 = F.generate_keys()
public_key4, private_key4 = F.generate_keys()

initiator = public_key0

energy_chain = B.BlockChain(initiator)

transact(public_key0, public_key1, private_key0, 975, public_key0)
transact(public_key0, public_key2, private_key0, 955, public_key0)
transact(public_key0, public_key3, private_key0, 100, public_key0)
transact(public_key3, public_key4, private_key3, 95, public_key0)
transact(public_key1, public_key4, private_key0, 5.0, public_key0)


energy_chain.blockchain_to_text()
# tx = E.Transaction(public_key0, receiver, amount)

# Creating Nodes
# for i in range(100):
#     F.generate_keys()

