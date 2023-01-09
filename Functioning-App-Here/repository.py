import sqlite3

def get_user_info_login(email, password):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT user_id, first_name FROM Users WHERE email = '{email}' AND password = '{password}'")
        return cur.fetchone()

def get_object_store():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT object_id, object_name, object_image_url, num_in_stock, description FROM Stock WHERE num_in_stock > 0")
        return cur.fetchall()

def add_obj_to_cart(user_id, object_id):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE Stock SET num_in_stock = num_in_stock - 1 WHERE object_id = {object_id}")
        cur.execute(f"SELECT object_id FROM CART WHERE user_id = {user_id} AND object_id = {object_id}")
        cart_info = cur.fetchone()
        if cart_info:
            cur.execute(f"UPDATE Cart SET num_in_cart = num_in_cart + 1 WHERE object_id = {object_id} AND user_id = {user_id}")
            return 
        cur.execute(f"INSERT INTO Cart(user_id, object_id, num_in_cart) VALUES({user_id}, {object_id}, 1)")

        conn.commit()
    return

def get_user_cart(user_id):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(f"""SELECT Stock.object_id, c.num_in_cart, Stock.object_name, Stock.description, Stock.object_image_url, Stock.object_name FROM 
        (
            SELECT * FROM Cart WHERE user_id = {user_id}
            ) AS c 
            INNER JOIN Stock ON c.object_id = Stock.object_id 
            WHERE c.num_in_cart > 0""")
        return cur.fetchall()

def remove_obj_from_cart(user_id, object_id):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE Stock SET num_in_stock = num_in_stock + 1 WHERE object_id = {object_id}")
        cur.execute(f"SELECT object_id FROM CART WHERE user_id = {user_id} AND object_id = {object_id}")
        cart_info = cur.fetchone()
        if cart_info:
                cur.execute(f"UPDATE Cart SET num_in_cart = num_in_cart - 1 WHERE object_id = {object_id} AND user_id = {user_id}")
                return 

        conn.commit()
    return