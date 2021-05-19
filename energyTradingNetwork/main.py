import ecosystem as E
import matplotlib.pyplot as plt

sim = E.Simulation('0h 5m 0s')
load_log, power_plant_log, dg_log, transaction_log = sim.run()
sim.Energy_chain.get_text()