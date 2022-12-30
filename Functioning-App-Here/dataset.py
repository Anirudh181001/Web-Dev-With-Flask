import sqlite3 
#Open database
conn = sqlite3.connect('./database.db')
from repository import get_object_store

import os
print(os.getcwd())


cur = conn.cursor()
cur.execute('''CREATE TABLE Users 
  (user_id INTEGER PRIMARY KEY, 
  password TEXT,
  email TEXT,
  first_name TEXT,
  last_name TEXT
  )''')

cur.execute('''CREATE TABLE Stock 
  (object_id INTEGER PRIMARY KEY, 
  object_name TEXT,
  object_image_url TEXT,
  num_in_stock INTEGER,
  description TEXT
  )''')

cur.execute('''CREATE TABLE Cart 
  (id INTEGER PRIMARY KEY, 
  object_id TEXT,
  user_id TEXT,
  num_in_cart INTEGER
  )''')

conn.commit()
stock = [
  ('Apple', 'https://img.freepik.com/free-photo/close-up-fresh-apple_144627-14640.jpg?w=1480&t=st=1672386110~exp=1672386710~hmac=532bb631755acb4ddba948c2acf8a198e18cbe12cc24b3e0cadfb061d5caef74', 20, 'A good excuse to stay away from medicine'),
  ('Banana', 'https://img.freepik.com/free-vector/vector-ripe-yellow-banana-bunch-isolated-white-background_1284-45456.jpg?w=2000&t=st=1672386638~exp=1672387238~hmac=add630fab78027cd022d102c205964d61729446a666ccac0569d6027ddf3be71', 20, 'Reminds me of Minions'),
  ('Pineapple', 'https://cdn.shopify.com/s/files/1/0707/2783/products/IMG_4307_copy_1000x.jpg?v=1447045653', 20, 'A good excuse to stay away from medicine, but thorny')
  ]
cur.execute("INSERT INTO Users(email, first_name, last_name, password) VALUES('anirudh@gmail.com', 'anirudh', 'shrinivason', 'password')")
conn.commit()
cur.executemany('''INSERT INTO Stock(object_name, object_image_url, num_in_stock, description) VALUES(?,?,?,?);''', stock)
conn.commit()

print(get_object_store())
