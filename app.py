from flask import Flask, render_template, request

app = Flask(__name__)

food_menu = {
    "Pizza": 120,
    "Burger": 80,
    "Pasta": 100,
    "Sandwich": 60,
    "Noodles": 90,
    "Biryani": 150,
    "Paneer Roll": 70,
    "Fries": 50
}

service_menu = {
    "Cleaning": 300,
    "Plumbing": 500,
    "Electric Repair": 450,
    "Painting": 800,
    "Appliance Installation": 600,
    "Furniture Assembly": 400
}

@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    query = request.args.get("q", "").lower()
    ordered_items = []
    total = 0
    payment_method = None  # New line

    filtered_food = {item: price for item, price in food_menu.items() if query in item.lower()}
    filtered_services = {item: price for item, price in service_menu.items() if query in item.lower()}

    if request.method == "POST":
        selected_food = request.form.getlist("food")
        selected_services = request.form.getlist("service")
        payment_method = request.form.get("payment_method")  # Get selected payment option

        for item in selected_food:
            if item in food_menu:
                ordered_items.append((item, food_menu[item]))
                total += food_menu[item]

        for item in selected_services:
            if item in service_menu:
                ordered_items.append((item, service_menu[item]))
                total += service_menu[item]

    return render_template("index.html",
                           food_menu=filtered_food,
                           service_menu=filtered_services,
                           ordered_items=ordered_items,
                           total=total,
                           query=query,
                           payment_method=payment_method)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
