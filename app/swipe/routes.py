from flask import render_template
from app.swipe import bp


dishes = [
    {
        "id": 1,
        "name": "Pasta Carbonara",
        "image": "pasta.jpeg",
        "price": "$12.99",
        "distance": "1 mile away",
        "rating": "4.5",
    },
    {
        "id": 2,
        "name": "Spaghetti Bolognese",
        "image": "spaghetti.jpeg",
        "price": "$10.99",
        "distance": "2 miles away",
        "rating": "4.0",
    },
    {
        "id": 3,
        "name": "Margherita Pizza",
        "image": "pizza.jpeg",
        "price": "$9.99",
        "distance": "3 miles away",
        "rating": "4.2",
    },
]


@bp.route("/")
def index():
    return render_template("./swiping/base.html")


@bp.route("/swipe")
def swipe():
    return render_template("./swiping/swipe.html", dishes=dishes)
