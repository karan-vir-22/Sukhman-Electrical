from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session handling

# Dummy users (in production, use a database)
users = {
    "admin": "admin123"
}

# Sample data
products = {
    "Switch": 30,
    "Socket": 40,
    "LED": 100,
    "Holder": 25,
    "Two Pin Plug": 15,
    "Three Pin Plug": 20,
    "MCB Switch": 150,
    "Wires": 10,
    "Fitting Pipes": 20
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
        return redirect(url_for("login"))

    query = request.args.get("q", "").lower()
    filtered_products = {item: price for item, price in products.items() if query in item.lower()}
    filtered_services = {item: price for item, price in services_available.items() if query in item.lower()}

    if request.method == "POST":
        ordered_items = []
        total = 0
        payment_method = request.form.get("payment_method")

        for item in products:
            qty = int(request.form.get(f"product_qty_{item}", 0))
            if qty > 0:
                total += qty * products[item]
                ordered_items.append((item, qty, qty * products[item]))

        for item in services_available:
            qty = int(request.form.get(f"service_qty_{item}", 0))
            if qty > 0:
                total += qty * services_available[item]
                ordered_items.append((item, qty, qty * services_available[item]))

        session['cart'] = ordered_items
        session['total'] = total
        session['payment_method'] = payment_method

    return render_template("index.html",
                           products=filtered_products,
                           services_available=filtered_services,
                           username=session.get("user"),
                           query=query)

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
            error = "Invalid username or password."

    return render_template("auth.html", error=error)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users:
            signup_error = "Username already exists. Please try a different one."
        else:
            users[username] = password
            session["user"] = username
            return redirect(url_for("index"))

    return render_template("signup.html", error=signup_error)

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = session.get("total", 0)
    return render_template("cart.html", cart_items=cart_items, total=total, username=session.get("user"))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_name = request.form.get('item_name')
    item_type = request.form.get('item_type')
    quantity = int(request.form.get('quantity', 1))
    action = request.form.get('action')  # 'add' or 'buy_now'

    # Get price from correct dictionary
    price = products.get(item_name) if item_type == 'product' else services_available.get(item_name)
    total_price = quantity * price if price else 0

    # Store the item in session
    cart = session.get('cart', [])
    cart.append({
        'name': item_name,
        'type': item_type,
        'quantity': quantity,
        'total_price': total_price
    })
    session['cart'] = cart

    # Recalculate total
    session['total'] = sum(item['total_price'] for item in cart)

    # Redirect based on button clicked
    if action == 'buy_now':
        return redirect(url_for('cart'))
    return redirect(url_for('index'))

@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    session.pop('total', None)
    return ('', 204)  # No content (for fetch to resolve without error)

@app.route("/about")
def about():
    return render_template("about.html", username=session.get("user"))

@app.route("/privacy")
def privacy_policy():
    return render_template("privacy.html")

@app.route("/terms")
def terms_conditions():
    return render_template("terms.html")

@app.route("/refund")
def refund_policy():
    return render_template("refund.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/process-payment', methods=['POST'])
def process_payment():
    if 'user' not in session:
        return redirect(url_for('login'))

    name = request.form.get('name')
    email = request.form.get('email')
    address = request.form.get('address')
    payment_method = request.form.get('paymentMethod')

    cart_items = session.get('cart', [])
    total = session.get('total', 0)

    # Optional: Print the order in terminal
    print(f"Order by {name} | ₹{total} | Payment: {payment_method}")
    print("Items:", cart_items)

    # Clear cart
    session.pop('cart', None)
    session.pop('total', None)

    return render_template('order_confirmation.html', name=name, total=total)



# ---------------------- Main ----------------------
if __name__ == "__main__":
    app.run(debug=True)
