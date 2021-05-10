from Modules import ecdsa, sqlite3, curve_type, hash_function, database_file, database_added, time, output_file_name, genesys_reward, halving_number, mining_reward

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = None

    def to_string(self):
        return self.sender + "---" + self.receiver + "---" + str(self.amount)

    @classmethod
    def from_string(cls, constructor_string):
        sender, receiver, amount = constructor_string.split("---")
        return cls(sender, receiver, amount)

    def sign_transaction(self, private_key_hex):
        global curve_type, hash_function

        signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve = curve_type, hashfunc = hash_function)
        signature = signing_key.sign(self.to_string().encode())
        self.signature = signature.hex()
        print("Successfully signed\n")


    def validate_balance(self):
        global database_file
        conn = sqlite3.connect(database_file)
        c = conn.cursor()
        cur_address = self.sender
        c.execute("""
                SELECT SUM(amount) 
                FROM transactions
                WHERE sender = :address;
            """, {'address': cur_address})
        entry = c.fetchone()
        debit = entry[0]


        c.execute("""
                SELECT SUM(amount) 
                FROM transactions
                WHERE receiver = :address;
            """, {'address': cur_address})
        entry = c.fetchone()
        credit = entry[0]
        conn.close()
        balance = credit if credit else 0.0 - debit if debit else 0.0
        print("Successfully validated balance\n")
        return balance >= self.amount
    
    def validate_signature(self):
        global curve_type, hash_function
        encoded_transaction_summary = self.to_string().encode()
        encoded_signature = bytes.fromhex(self.signature)
        flag = False
        try:
            verifying_key = ecdsa.VerifyingKey.from_string(
                                                            bytes.fromhex(self.sender), 
                                                            curve = curve_type, 
                                                            hashfunc = hash_function
                                                        )
            verifying_key.verify(
                                    encoded_signature, 
                                    encoded_transaction_summary
                                )
            flag = True
        except:
            pass
        print("Successfully validated signature\n")
        return flag

    def to_mempool(self, mempool):
        return mempool.push(self)

class Mempool:
    def __init__(self):
        self.mempool = []
    def push(self, transaction):
        try:
            self.mempool.append(transaction)
            return True
        except:
            pass
        return False

    def pop(self):
        return self.mempool.pop(0)

    def empty(self):
        return True if len(self.mempool) == 0 else False

class Block:
    def __init__(self):
        self.list_of_transactions = []
        self.previous_block_Key = 0
        self.current_Key = None
        self.next = None
        self.time_stamp = time()
        self.nonce = None
        self.miner = None
        self.mining_reward = 0

    def push_transaction(self, transaction):
        if transaction.validate_balance() and transaction.validate_signature():
            # print("Success")
            self.list_of_transactions.append(transaction)
            return True
        return False

    def set_previous_key(self,previous_block_Key):
        self.previous_block_Key = previous_block_Key

    def hash(self):
        self.current_Key = hash(self)

    def get_hash(self):
        return self.current_Key

    def set_miner(self, miner):
        self.miner = miner

    def set_mining_reward(self, mining_reward):
        self.mining_reward = mining_reward

    def set_nonce(self):
        pass

    def write_block_data(self):
        global output_file_name
        f = open(output_file_name, 'a')
        f.write("\n\ntimestamp: {}\nBlock Hash: {}\n".format(self.time_stamp, self.current_Key))
        for tx in self.list_of_transactions:
            f.write("Sender: {}\nReceiver: {}\nAmount: {}\n\n".format(tx.sender, tx.receiver, tx.amount))
        f.write("Block Reward: {}\nReceiver: {}\n\n".format(self.mining_reward, self.miner))
        f.write("--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--:--")
        f.close()

class BlockChain:
    global genesys_reward, mining_reward, halving_number, database_file

    def __init__(self, initiator_account):
        self.genesis_block = Block()
        self.initiator_account = initiator_account
        self.tail_block = None
        self.length = 0
        self.mining_reward = genesys_reward
        self.mine(self.genesis_block, initiator_account)

    def mine(self, block, miner):
        if(block != self.genesis_block and len(block.list_of_transactions) == 0):
            return False
        block.set_mining_reward(self.mining_reward)
        block.set_miner(miner)

        if self.tail_block:
            block.set_previous_key(self.tail_block.get_hash())

            self.tail_block.next = block

        else:
            # gensys block
            block.set_previous_key('0')

            # self.tail_block.next = block
        
        self.tail_block = block
        self.tail_block.hash()

        self.length += 1
        if(self.length % halving_number == 0):
            mining_reward /= 2                                                              # Halving

        conn = sqlite3.connect(database_file)
        c = conn.cursor()
        for tx in block.list_of_transactions:
            c.execute("INSERT INTO transactions VALUES(:sender, :receiver, :amount)",
                {
                    'sender':  tx.sender,
                    'receiver':tx.receiver,
                    'amount':  tx.amount
                }
            )
        
        c.execute("INSERT INTO transactions VALUES(:sender, :receiver, :amount)",
            {
                'sender':  '0',
                'receiver':miner,
                'amount':  self.mining_reward
            }
        )

        conn.commit()
        conn.close()
        return True


    def competetive_mine(block):
        """
            This function is responsible for getting a nonce and
            competetively mine the block. 
        """
        pass

    def get_text(self):
        temp = self.genesis_block
        while temp:
            temp.write_block_data()
            temp = temp.next  