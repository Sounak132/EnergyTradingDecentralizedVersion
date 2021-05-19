from Modules import curve_type, hash_function, database_file
import ecdsa, sqlite3
import blockchain as B
from operator import attrgetter

def generate_database():
    # declaring the global variables
    global database_added, database_file

    # if database_added == 0:
    # Create the database
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    c.execute("""CREATE TABLE transactions (
        sender TEXT NOT NULL,
        receiver TEXT NOT NULL,
        amount FLOAT NOT NULL
    )""")

    c.execute("""CREATE TABLE credentials (
        public_key TEXT NOT NULL,
        private_key TEXT NOT NULL,
        PRIMARY KEY(public_key)
    )""")

    conn.commit()
    conn.close()
    # database_added = 1

def generate_keys():
    # declaring the global variables
    global database_file

    private_key = ecdsa.SigningKey.generate(curve = curve_type, hashfunc= hash_function)
    public_key = private_key.verifying_key

    public_key_hex = public_key.to_string().hex()
    private_key_hex = private_key.to_string().hex()

    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Add the generated keys to the database
    c.execute(
                "INSERT INTO credentials VALUES(:public_key, :private_key)", 
                {
                    'public_key': public_key_hex, 
                    'private_key': private_key.to_string().hex()
                }
            )
    conn.commit()
    conn.close()
    return public_key_hex

def to_time(run_time):
    hour, _ = run_time.split('h')
    minute, _ = _.split('m') 
    second, _ = _.split('s') 
    return int(hour)*3600 + int(minute)*60 + int(second)

def average_minimum(obj_list, attr):
    if len(obj_list) == 0:
        return None, None, None
    average_attr = 0
    num = 0
    getter = attrgetter(attr)
    minimum = obj_list[0]
    index = 0
    for obj in obj_list:
        cur_attr = getter(obj)
        if cur_attr < getter(minimum):
            minimum = obj
            index = num
        average_attr += getter(obj)
        num += 1
    return average_attr/num, minimum, index