from Modules import database_file
import sqlite3, random
from time import time
import blockchain as B
import functions as F
from operator import attrgetter


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
        # return new_block if flag1 and flag2 else None
        return flag1 and flag2

class EnergyNode(Node):
    def __init__(self, public_key):
        super().__init__(public_key = public_key)
        self.max_production_rate  = 0            # units/ hour
        self.max_consumption_rate = 0            # units/hour
        self.max_battery_capacity = 0            # units

        self.production_rate  = 0                # units/ hour
        self.consumption_rate = 0                # units/hour
        self.battery_holding  = 0                # units

        self.selling_price = 100 *(1 + random.randint(0, 30)/100)


    def set_max_production_rate(self, max_production_rate):
        self.max_production_rate  = max_production_rate

    def set_max_consumption_rate(self, max_consumption_rate):
        self.max_consumption_rate = max_consumption_rate
    
    def set_max_battery_capacity(self, max_battery_capacity):
        self.max_battery_capacity = max_battery_capacity
    
    # This function will activate the node
    def switch_on(self):
        self.production_rate  = random.randint(500, 1000)/1000 * self.max_production_rate
        self.consumption_rate = random.randint(500, 1000)/1000 * self.max_consumption_rate
        self.battery_holding  = 0

    def switch_off(self):
        self.production_rate  = 0
        self.consumption_rate = 0

    def refresh(self, supply, time_elapsed):
        op = 1 if random.randint(0,100)>=50 else -1
        self.consumption_rate = max(0, (1 + op * random.randint(0,30)/100) * self.consumption_rate)

        op = 1 if random.randint(0,100)>=50 else -1
        self.production_rate  = max(0, (1 + op * random.randint(0,30)/100) * self.production_rate)

        if supply == 0:
            self.consumption_rate = min( self.consumption_rate * time_elapsed , self.battery_holding)

        self.consumption_rate = min(self.consumption_rate, self.max_consumption_rate)
        self.production_rate  = min(self.production_rate,  self.max_production_rate)
    
    def refresh_battery(self, time_elapsed):
        self.battery_holding += (self.production_rate - self.consumption_rate) * time_elapsed
        self.battery_holding  = min(self.battery_holding, self.max_battery_capacity)
    
    def refresh_cost(self, average_selling_price): 
        op = 1 if random.randint(0, 100) > 50 else -1
        profit = op * random.randint(0,20)/100 * average_selling_price
        self.selling_price += profit
        

class PowerPlant:
    def __init__(self, production_rate):
        self.production_rate = production_rate
    def switch_on(self):
        pass
    def refresh(self, production_rate):
        self.production_rate = production_rate
        

class SubEcosystem:
    def __init__(
            self, 
            num_nodes, 
            max_production_rate, 
            max_consumption_rate, 
            max_battery_capacity, 
            initial_set_balance, 
            initiator_node, 
            Energy_chain,
            mempool
        ):            # num_nodes --> number of initializing nodes 

        self.list_of_nodes    = []
        self.source = 0
        self.running = 0
 
        for i in range(num_nodes):
            public_key_i = F.generate_keys()
            new_node = EnergyNode(public_key_i)

            # set initial balance for the nodes
            initiator_node.initiate_transaction(new_node.public_key, initial_set_balance, mempool)
            initiator_node.mine(mempool = mempool, blockchain = Energy_chain)

            # set maximum attributes
            max_production_rate_i  = random.randint(0, 100)/100 * max_production_rate
            max_consumption_rate_i = random.randint(0, 100)/100 *max_consumption_rate
            max_battery_capacity_i = random.randint(0, 100)/100 *max_battery_capacity
            
            new_node.set_max_production_rate(max_production_rate_i)
            new_node.set_max_consumption_rate(max_consumption_rate_i)
            new_node.set_max_battery_capacity(max_battery_capacity_i)
            
            self.list_of_nodes.append(new_node)

    def switch_on(self):
        for node in self.list_of_nodes:
            node.switch_on()
        self.running = 1
    
    def get_total_load(self):
        load = 0
        for node in self.list_of_nodes:
            load += node.consumption_rate
        return load
    
    def refresh(self, time_elapsed):
        for node in self.list_of_nodes:
            node.refresh(self.running, time_elapsed)
            node.refresh_battery(time_elapsed)

class Ecosystem:
    def __init__(self, list_of_sub_ecosystems, power_plant):
        self.list_of_sub_ecosystems = list_of_sub_ecosystems
        self.power_plant = power_plant
    def switch_on(self):
        for sub_eco_system in self.list_of_sub_ecosystems:
            sub_eco_system.switch_on();
        load = 0
        for sub_eco in self.list_of_sub_ecosystems:
            load += sub_eco.get_total_load()
        PowerPlant.switch_on(load)

class Simulation:
    def __init__(self, run_time):

        F.generate_database()           # initiate the database

        initiator_public_key  = F.generate_keys()
        self.initiator_node   = Node(initiator_public_key)
        self.Energy_chain     = B.BlockChain(initiator_public_key)
        self.mempool          = B.Mempool()

        self.run_time = F.to_time(run_time)
        # self.load_shedding_interval = load_shedding_interval
        # ---|- 0% -|--- successful start -|- 50% -|- load shedding -|- 60% -|- load restored -|- end of simulation 100%

        self.list_of_sub_ecosystems = []
        self.ecosystem = None

    def time_lapsed(self, start):
        return time()-start

    def run(self):
        load_log = []
        dg_log = []
        power_plant_log = []

        transaction_log = []
        # battery_charge_log = []

        self.list_of_sub_ecosystems = [
            SubEcosystem(100, 0.01, 0.00833, 5, 100, self.initiator_node, self.Energy_chain, self.mempool),
            SubEcosystem(200, 0.01, 0.00833, 5, 100, self.initiator_node, self.Energy_chain, self.mempool),
            SubEcosystem(100, 0.01, 0.00833, 5, 100, self.initiator_node, self.Energy_chain, self.mempool),
            SubEcosystem(50,  0.01, 0.00833, 5, 100, self.initiator_node, self.Energy_chain, self.mempool)
        ]
        self.ecosystem = Ecosystem(self.list_of_sub_ecosystems, PowerPlant(4))
        self.ecosystem.switch_on()
        start = time()

        time_flag = time()
        refresh_interval   = 0.4
        battery_lower_threshold = 1
        battery_upper_threshold = 2.5

        # super loop
        while (self.time_lapsed(start) <= self.run_time):
            print(self.time_lapsed(start))
            if(self.time_lapsed(start) >= self.run_time*0.5 and self.time_lapsed(start) <= self.run_time*0.75):
                self.list_of_sub_ecosystems[0].running = 0
                self.list_of_sub_ecosystems[-1].running = 0
            else:
                self.list_of_sub_ecosystems[0].running = 1
                self.list_of_sub_ecosystems[-1].running = 1
            
            load_powerplant = 0
            load_dg = 0
            trade_requests = []
            sources = []

            # refresh loads and sources
            if(self.time_lapsed(time_flag) >= refresh_interval):
                
                for sub_eco in self.ecosystem.list_of_sub_ecosystems:
                    sub_eco.refresh(self.time_lapsed(time_flag))            # time lapsed from last updated time flag
                    status = sub_eco.running                                # is this sub ecosystem connected to grid?
                    if(status == 1):
                        # If grid is supplying power
                        load_powerplant += sub_eco.get_total_load()
                        for node in sub_eco.list_of_nodes:
                            if node.battery_holding >= battery_upper_threshold :
                                if random.randint(0,100) <70:
                                    sources.append(node)
                    else:
                        # If the system is running on DG
                        load_dg += sub_eco.get_total_load()
                        for node in sub_eco.list_of_nodes:
                            if node.battery_holding <= battery_lower_threshold :
                                if random.randint(0,100) <90:
                                    trade_requests.append(node)

                    sub_eco.refresh(self.time_lapsed(time_flag))

                self.ecosystem.power_plant.refresh(load_powerplant)
                power_plant_log.append(load_powerplant)
                dg_log.append(load_dg)
                load_log.append(load_dg + load_powerplant)

            
            # Trade
            num_trade = 0
            if len(trade_requests) > 0 and len(sources) > 0:
                average_selling_price, cur_source, index = F.average_minimum(sources, 'selling_price')
                for requester in trade_requests:
                    price = cur_source.selling_price/1000
                    traded_energy = 1/1000
                    miner_eco = self.list_of_sub_ecosystems[random.randint(0, len(self.list_of_sub_ecosystems)-1)]
                    miner = miner_eco.list_of_nodes[random.randint(0, len(miner_eco.list_of_nodes)-1)]
                    while True:
                        if (cur_source.battery_holding - traded_energy < battery_lower_threshold):
                            sources.pop(index)
                            average_selling_price, cur_source, index = F.average_minimum(sources, 'selling_price')
                        else:
                            break
                    
                    # payment
                    requester.initiate_transaction(cur_source.public_key, price, self.mempool)

                    # Data added to blockchain
                    if (miner.mine(self.mempool, self.Energy_chain)):
                        cur_source.battery_holding -= traded_energy
                        requester.battery_holding  += traded_energy
                        num_trade += 1

                for sub_eco in self.list_of_sub_ecosystems:
                    for node in sub_eco.list_of_nodes:
                        node.refresh_cost(average_selling_price)   
                        
            transaction_log.append(num_trade)

            time_flag = time()        
        return load_log, power_plant_log, dg_log, transaction_log