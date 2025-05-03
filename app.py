from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample user storage (Replace with a database in production)
users = {}

# Sample data
products = {
    "Switch": 30,
    "Socket": 40,
    "LED" : 100,
    "Holder": 25,
    "Two Pin Plug": 15,
    "Three Pin Plug": 20,
    "MCB Switch": 150,
    "Wires": 10,  # per meter
    "Fitting Pipes": 20  # per meter
}

services_available = {
    "Home Electrical Installation": 500,
    "Repair Service": 400,
    "Wiring Repair": 500,
    "AC Installation": 1500,
    "Switch Board Fitting": 350
}

# ---------------------- Routes ----------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("signup"))  # Force users to sign up first!

    query = request.args.get("q", "").lower()
    filtered_products = {item: price for item, price in products.items() if query in item.lower()}
    filtered_services = {item: price for item, price in services_available.items() if query in item.lower()}

    if request.method == "POST":
        ordered_items = []
        total = 0
        payment_method = request.form.get("payment_method")

        # Products
        for item in products:
            qty = int(request.form.get(f"product_qty_{item}", 0))
            if qty > 0:
                price = products[item]
                total += qty * price
                ordered_items.append((item, qty, qty * price))

        # Services
        for item in services_available:
            qty = int(request.form.get(f"service_qty_{item}", 0))
            if qty > 0:
                price = services_available[item]
                total += qty * price
                ordered_items.append((item, qty, qty * price))

        session['cart'] = ordered_items
        session['total'] = total
        session['payment_method'] = payment_method

    return render_template("index.html",
                           products=filtered_products,
                           services_available=filtered_services,
                           username=session.get("user"),
                           query=query)
@app.route("/about")
def about():
    return render_template("about.html", username=session.get("user"))

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = sum(price for item, qty, price in cart_items)  # Fixed unpacking issue
    return render_template("cart.html", cart_items=cart_items, total=total, username=session.get("user"))




@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users:
            error = "Username already exists. Please try a different one."
        else:
            users[username] = password
            session["user"] = username
            return redirect(url_for("index"))  # Redirect to homepage after signup

    return render_template("signup.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            error = "Account not found. Please sign up first."
            return redirect(url_for("signup"))  # Redirect to signup if user isn't registered

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("cart", None)
    session.pop("total", None)
    session.pop("payment_method", None)
    return redirect(url_for("signup"))  # Force users to go through signup again!

# ---------------------- Main ----------------------

if __name__ == "__main__":
    app.run(debug=True)