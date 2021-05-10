from Modules import database_file, sqlite3, random
import blockchain as B
import functions as F

class Node:
    def __init__(self, public_key):
        self.public_key = public_key
    
    def initiate_transaction(self, receiver_public_key, amount, mempool):
        tx = B.Transaction(self.public_key, receiver_public_key, amount)
        conn = sqlite3.connect(database_file)
        c = conn.cursor()
        c.execute("SELECT private_key FROM credentials WHERE public_key = :public_key",{'public_key': self.public_key})
        private_key = c.fetchone()[0]
        tx.sign_transaction(private_key)
        tx.to_mempool(mempool)
        return tx

    def mine(self, mempool, blockchain):
        new_block = B.Block()
        tx = mempool.pop()
        flag1 = new_block.push_transaction(tx)
        flag2 = False
        if flag1:
            flag2 = blockchain.mine(new_block, self.public_key)
        return new_block if flag1 and flag2 else None

class EnergyNode(Node):
    def __init__(self, public_key):
        super().__init__(public_key = public_key)
        self.max_production_rate = 0            # units/ hour
        self.max_consumption_rate = 0           # units/hour
        self.max_battery_capacity = 0           # units

        self.production_rate = 0                # units/ hour
        self.consumption_rate = 0               # units/hour
        self.battery_holding = 0                # units

    def set_max_production_rate(self, max_production_rate):
        self.max_production_rate = max_production_rate

    def set_max_consumption_rate(self, max_consumption_rate):
        self.max_consumption_rate = max_consumption_rate
    
    def set_max_battery_capacity(self, max_battery_capacity):
        self.max_battery_capacity = max_battery_capacity
    
    # This function will activate the node
    def switch_on(self):
        pass
    def switch_off(self):
        pass

class PowerPlant:
    def __init__(self, productionRate):
        self.productionRate = productionRate

class Ecosystem:
    def __init__(self, num, max_production_rate, max_consumption_rate, max_battery_capacity, initial_set_balance):            # num --> number of initializing nodes 
        F.generate_database()           # initiate the database

        self.list_of_nodes    = []
        initiator_public_key  = F.generate_keys()
        self.initiator_node   = Node(initiator_public_key)
        self.Energy_chain     = B.BlockChain(initiator_public_key)
        self.mempool          = B.Mempool()

        for i in range(num):
            public_key_i = F.generate_keys()
            new_node = EnergyNode(public_key_i)

            # set initial balance for the nodes
            self.initiator_node.initiate_transaction(new_node.public_key, initial_set_balance, self.mempool)
            self.initiator_node.mine(mempool = self.mempool, blockchain = self.Energy_chain)

            # set maximum attributes
            max_production_rate_i  = random.randint(0, max_production_rate)
            max_consumption_rate_i = random.randint(0, max_consumption_rate)
            max_battery_capacity_i = random.randint(0, max_battery_capacity)
            
            new_node.set_max_production_rate(max_production_rate_i)
            new_node.set_max_consumption_rate(max_consumption_rate_i)
            new_node.set_max_battery_capacity(max_battery_capacity_i)
            
            self.list_of_nodes.append(new_node)

        def switch_on(self):
            pass