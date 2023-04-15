from flask import render_template, redirect, request, make_response, jsonify
from uuid import uuid4

from app.routes.swipe import bp
from app.models.swipe import Swipe
from app.models.meal import Meal
from app.extensions import db
import json


dishes = [
    {
        "uuid": str(uuid4()),
        "name": "Pasta Carbonara",
        "picture": "pasta.jpeg",
        "price": 12.99,
        "user_id": 1,
    },
    {
        "uuid": str(uuid4()),
        "name": "Spaghetti Bolognese",
        "picture": "spaghetti.jpeg",
        "price": 10.99,
        "user_id": 1,
    },
    {
        "uuid": str(uuid4()),
        "name": "Margherita Pizza",
        "picture": "pizza.jpeg",
        "price": 9.99,
        "user_id": 1,
    },
    {
        "uuid": str(uuid4()),
        "name": "Pasta",
        "picture": "pasta.jpeg",
        "price": 12.99,
        "user_id": 1,
    },
    {
        "uuid": str(uuid4()),
        "name": "Rice",
        "picture": "pasta.jpeg",
        "price": 12.99,
        "user_id": 1,
    },
]


@bp.route("/")
def index():
    mealsExist = len(Meal.query.all())
    if not mealsExist:
        for dish in dishes:
            newMeal = Meal(**dish)
            db.session.add(newMeal)

        db.session.commit()

    meals = (
        Meal.query.filter(
            Meal.id.notin_(db.session.query(Swipe.meal_id).filter_by(user_id=1))
        )
        .limit(3)
        .all()
    )

    return render_template("./swipe/swipe.html", meals=meals)


@bp.route("/swipe/<string:uuid>/<string:direction>", methods=["POST"])
def swipe(uuid, direction):
    """
    A route for showing and handling swipe requests for meals

    GET method will display three random meals that are not in the swipe table yet
    POST method will handle swipes and add them to the swipe table

    Returns:
        A rendered template containing the swipe page with three random meals
    """
    # Get the user ID from the session
    # user_id = db.session.get("user_id")
    meal = Meal.query.filter_by(uuid=uuid).first()
    print(meal)

    # Add a new swipe to the database
    swipe = Swipe(uuid=str(uuid4()), direction=direction, user_id=1, meal_id=meal.id)
    db.session.add(swipe)
    db.session.commit()

    # Redirect to the previous page
    # Get three random meals that are not in the swipe table yet
    query = (
        Meal.query.filter(
            Meal.id.notin_(db.session.query(Swipe.meal_id).filter_by(user_id=1))
        )
        .limit(3)
        .all()
    )

    meals = [meal.as_dict() for meal in query]

    return make_response({"message": "Meal swipped successfully", "data": meals}, 200)
