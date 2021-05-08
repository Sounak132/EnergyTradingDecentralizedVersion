database_file = 'testdb.db'
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
        self.signature = None

    def to_string(self):
        return self.sender + "---" + self.receiver + "---" + str(self.amount)

    @classmethod
    def from_string(cls, constructor_string):
        sender, receiver, amount = constructor_string.split("---")
        return cls(sender, receiver, amount)

    def sign_transaction(self, private_key_hex):
        transaction_summary = self.to_string()
        signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex))
        signature = signing_key.sign(transaction_summary.encode())
        self.signature = signature.hex()


    def validate_balance(self):
        conn = sqlite3.connect(database_file)
        c = conn.cursor()
        cur_address = self.sender
        c.execute("""
                SELECT SUM(amount) 
                FROM transactions
                WHERE sender = :address;
            """, {'address': cur_address})
        entry = c.fetchone()
        debit = entry


        c.execute("""
                SELECT SUM(amount) 
                FROM transactions
                WHERE receiver = :address;
            """, {'address': cur_address})
        entry = c.fetchone()
        conn.close()
        credit = entry
        balance = credit - debit
        return balance >= self.amount
    
    def validate_signature(self):
        encoded_transaction_summary = self.to_string().encode()
        encoded_signature = bytes.fromhex(self.signature)
        flag = False
        try:
            verifying_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender))
            verifying_key.verify(encoded_signature, encoded_transaction_summary)
            flag = True
        except:
            pass
        return flag


class Block:
    def __init__(self, previous_Key):
        self.list_of_transactions = []
        self.previous_block_Key = previous_Key
        self.current_Key = None
        self.next = None
        self.time_stamp = time()

    def pushT(self, transaction):
        if transaction.validate():
            self.list_of_transactions.append(transaction)

    def get_hash(self):
        self.current_Key = hash(self)
        return self.current_Key
    
        
        

class BlockChain:
    def __init__(self, head):
        GenesysBlock = Block()
        self.head = GenesysBlock
    def pushB(block):
        # if (b.validate() == True):
        #     key = 

        pass

    def generate_keys(curve_type):
        sk = SigningKey.generate(curve = curve_type)
        vk = sk.verifying_key

        return (sk.to_string().hex(), vk.to_string().hex())

    def get_public_key(public_hex, curve_type):
        return VerifyingKey.from_string(bytes.fromhex(public_hex), curve=curve_type)

    def get_private_key(private_hex, curve_type):
        return SigningKey.from_string(bytes.fromhex(private_hex), curve=curve_type)