import sqlite3 
#Open database
conn = sqlite3.connect('./database.db')


import os
print(os.getcwd())

cur = conn.cursor()
# cur.execute('''CREATE TABLE users 
#   (userId INTEGER PRIMARY KEY, 
#   password TEXT,
#   email TEXT,
#   firstName TEXT,
#   lastName TEXT
#   )''')

# cur.execute('''INSERT INTO users (password, email, firstName, lastName) VALUES('password', 'anirudh@gmail.com', 'anirudh', 'shrinivason')''')
# conn.commit()
