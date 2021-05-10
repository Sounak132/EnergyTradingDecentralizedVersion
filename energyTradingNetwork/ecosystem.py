class House:
    def __init__(self, production_rate, consumption_rate, batteryHolding, address, balance):
        self.production_rate = production_rate
        self.consumption_rate = consumption_rate
        self.batteryHolding = batteryHolding
        self.address = address
        self.balance = balance
    

class PowerPlant:
    def __init__(self, productionRate):
        self.productionRate = productionRate