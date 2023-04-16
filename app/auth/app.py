from flask import Flask
from flask import render_template

app = Flask(__name__)
dishes = [
    {
        "id":1, 
        "name": "Pasta Carbonara",
        "image": "pasta.jpeg",
        "price": "$12.99",
        "distance": "1 mile away",
        "rating": "4.5"
    },
    {
        "id": 2, 
        "name": "Spaghetti Bolognese",
        "image": "spaghetti.jpeg",
        "price": "$10.99",
        "distance": "2 miles away",
        "rating": "4.0"
    },
    {
        "id": 3, 
        "name": "Margherita Pizza",
        "image": "pizza.jpeg",
        "price": "$9.99",
        "distance": "3 miles away",
        "rating": "4.2"
    }
]
@app.route('/')
def index():
    return render_template("base.html")


@app.route('/swipe')
def swipe():
    return render_template("swipe.html", dishes=dishes)

if __name__ =="__main__":
    app.run(host='0.0.0.0', port=81)

