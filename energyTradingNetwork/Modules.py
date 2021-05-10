import ecdsa
from ecdsa import SECP256k1 as curve_type
from hashlib import sha256 as hash_function
import sqlite3
from time import time

database_file = 'testdb.db'
database_added = 0
genesys_reward = 1024
halving_number = 10000 # 10240000 + 512
mining_reward = 0
output_file_name = 'op.txt'