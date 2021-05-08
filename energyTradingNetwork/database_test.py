import sqlite3

conn = sqlite3.connect('testdb.db')
c = conn.cursor()

# c.execute("""CREATE TABLE transactions (
#     sender TEXT NOT NULL,
#     receiver TEXT NOT NULL,
#     amount FLOAT
# )""")

# c.execute("""CREATE TABLE credentials (
#     public_key TEXT NOT NULL,
#     private_key TEXT NOT NULL,
#     balance FLOAT,
#     PRIMARY KEY(public_key)
# )""")

# c.execute("INSERT INTO transactions VALUES('dgjbcfjeblfhbclifkje', 'eifvgbcelirufbdcilkhjnliudjc', 1.098756)")
# c.execute("INSERT INTO transactions VALUES('dgjbcfjeblfhbclifkje', 'eifvgbcelirufbdcilkhjnliudjc', 10.0987)")
# c.execute("INSERT INTO transactions VALUES('dgjbcfjeblfhbclifkje', 'eifvgbcelirufbdcilkhjnliudjc', 5.0987)")
# c.execute("INSERT INTO transactions VALUES('eifvgbcelirufbdcilkhjnliudjc', 'dgjbcfjeblfhbclifkje', 4.0987)")
# c.execute("INSERT INTO transactions VALUES('dgjbcfjeblfhbclifkje', 'eifvgbcelirufbdcilkhjnliudjc', 3.0987)")
# c.execute("INSERT INTO transactions VALUES('eifvgbcelirufbdcilkhjnliudjc', 'dgjbcfjeblfhbclifkje', 2.0987)")
# c.execute("INSERT INTO transactions VALUES('dgjbcfjeblfhbclifkje', 'eifvgbcelirufbdcilkhjnliudjc', 1.0987)")
# c.execute("INSERT INTO transactions VALUES('dgjbcfjeblfhbclifkje', 'eifvgbcelirufbdcilkhjnliudjc', 3.0987)")
# c.execute("INSERT INTO transactions VALUES('eifvgbcelirufbdcilkhjnliudjc', 'dgjbcfjeblfhbclifkje', 2.0987)")
# c.execute("INSERT INTO transactions VALUES('dgjbcfjeblfhbclifkje', 'eifvgbcelirufbdcilkhjnliudjc', 1.0987)")
# c.execute("INSERT INTO transactions VALUES('dgjbcfjeblfhbclifkje', 'eifvgbcelirufbdcilkhjnliudjc', 4.0987)")
# c.execute("INSERT INTO transactions VALUES('eifvgbcelirufbdcilkhjnliudjc', 'dgjbcfjeblfhbclifkje', 4.0987)")
# c.execute("INSERT INTO transactions VALUES('dgjbcfjeblfhbclifkje', 'eifvgbcelirufbdcilkhjnliudjc', 8.0987)")
# c.execute("INSERT INTO transactions VALUES('eifvgbcelirufbdcilkhjnliudjc', 'dgjbcfjeblfhbclifkje', 11.0987)")


# c.execute("INSERT INTO credentials VALUES('dgjbcfjeblfhbclifkje', 'eifvgbcelirufbdcilkhjnliudjc', 1.0987)")

cur_address = "dgjbcfjeblfhbclifkje"
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
credit = entry

balance = credit[0] - debit[0]
print("Balance of user: {} is {} ".format(cur_address, balance))

# c.execute("SELECT * FROM credentials")

# entry = c.fetchone()
# print(entry, type(entry))


conn.commit()
conn.close()