from Modules import ecdsa, sqlite3, curve_type, hash_function, database_file
import blockchain as B

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