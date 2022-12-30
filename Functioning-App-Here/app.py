from flask import Flask, redirect, render_template, request, url_for
from repository import (
    get_user_info_login,
    get_object_store,
    add_obj_to_cart,
    get_user_cart,
    remove_obj_from_cart
)

app = Flask(__name__)

# Can get this information from cookie if we store email in cookie
LOGGED_IN = False
USERNAME = ""
USER_ID = None


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
        global LOGGED_IN, USERNAME, USER_ID
        LOGGED_IN = True
        USERNAME = user_info[1]
        USER_ID = user_info[0]
        return redirect(url_for("success", name=USERNAME))
    else:
        return render_template("login.html")


@app.route("/success/<name>")
def success(name):
    cart_infos = get_object_store()
    return render_template("home.html", username=name, cart_infos=cart_infos)


@app.route("/")
def home():
    if not LOGGED_IN:
        return redirect(url_for("login"))
    return redirect(url_for("success", name=USERNAME))


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    object_ids = request.form.keys()
    for object_id in object_ids:
        add_obj_to_cart(USER_ID, object_id)
    return redirect(url_for("success", name=USERNAME))

@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    object_ids = request.form.keys()
    for object_id in object_ids:
        remove_obj_from_cart(USER_ID, object_id)
    return redirect(url_for("view_cart"))


@app.route("/cart")
def view_cart():
    print("HELLOOO")
    cart_infos = get_user_cart(USER_ID)
    print(cart_infos)
    return render_template("cart.html", cart_infos=cart_infos, username=USERNAME)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
