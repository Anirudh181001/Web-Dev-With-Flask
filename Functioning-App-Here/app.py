from flask import Flask, redirect, render_template, request, url_for, session 
from repository import (
    get_user_info_login,
    get_object_store,
    add_obj_to_cart,
    get_user_cart,
    remove_obj_from_cart
)

app = Flask(__name__)
app.secret_key = "Anirudh is the coolest"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_info = get_user_info_login(email, password)
        if not user_info:
            return render_template(
                "login.html", error_message="Invalid login credentials"
            )
        session['username'] = user_info[1]
        session['user_id'] = user_info[0]
        return redirect(url_for("success"))
    else:
        return render_template("login.html")


@app.route("/success")
def success():
    cart_infos = get_object_store()
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template("home.html", username=session['username'], cart_infos=cart_infos)


@app.route("/")
def home():
    if 'username' not in session:
        return redirect(url_for("login"))
    return redirect(url_for("success"))


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    object_ids = request.form.keys()
    for object_id in object_ids:
        add_obj_to_cart(session['user_id'], object_id)
    return redirect(url_for("success", name=session['username']))

@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    object_ids = request.form.keys()
    for object_id in object_ids:
        remove_obj_from_cart(session['user_id'], object_id)
    return redirect(url_for("view_cart"))


@app.route("/cart")
def view_cart():
    cart_infos = get_user_cart(session['user_id'])
    print(cart_infos)
    return render_template("cart.html", cart_infos=cart_infos, username=session['username'])


if __name__ == "__main__":
    app.run(debug=True, port=8080)
