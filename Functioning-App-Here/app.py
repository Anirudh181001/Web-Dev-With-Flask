from urllib import parse
from flask import Flask, redirect, render_template, request, session, url_for
from views import views
import sqlite3, hashlib, os

app = Flask(__name__)
app.register_blueprint(views, url_prefix='/views')

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (session['email'], ))
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM kart WHERE userId = ?", (userId, ))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT userId, firstName FROM users WHERE email = '{email}'")
            userId, firstName = cur.fetchone()
        return redirect(url_for('success', name=firstName))
    else:
        return render_template('login.html')

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route('/')
def home2():
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData) 
    return render_template('home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData)


if __name__ == '__main__':
    app.run(debug=True, port=8080)