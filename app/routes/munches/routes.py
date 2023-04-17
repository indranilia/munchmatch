from flask import render_template
from app.models.meal import Meal
from app.models.swipe import Swipe
from app.models.review import Review
from sqlalchemy import func
from app.jwt import token_required
from app.routes.munches import bp


@bp.route("/munches/")
@token_required
def get_munch():
    """
    Get information about munches, including the cheapest, most relevant, and closest ones.

    Returns:
    --------
    A rendered HTML template that displays information about the munches:
    - munches: a list of all munches that have been swiped right by users
    - cheapest_munch: the cheapest munch that has been swiped right by users
    - relevant_munch: the most relevant munch that has been swiped right by users, based on the average rating from reviews
    - closest_munch: 
    """
    munches = Meal.query \
    .join(Swipe)\
    .filter(Swipe.direction == 'right')\
    .all()
    cheapest_munch = Meal.query \
    .join(Swipe) \
    .filter(Swipe.direction == 'right') \
    .order_by(Meal.price.asc()) \
    .first()
    relevant_munch = Meal.query \
    .join(Swipe) \
    .join(Review) \
    .filter(Swipe.direction == 'right') \
    .group_by(Meal.id) \
    .with_entities(Meal, func.avg(Review.rating).label('avg_rating')) \
    .order_by(func.avg(Review.rating).desc()) \
    .first()
    #closest_munch = to be added via google map reference
    return render_template("meal/munches.html", munches=munches, cheapest_munch=cheapest_munch, relevant_munch=relevant_munch, closest_munch=closest_munch)


@bp.route("/munch/<int:id>/")
@token_required
def get_munch(id):
    """
    Get a munch with a given id 
    Parameters
    -----------
    - id: post id
    Returns
    -----------
    Munch with given id
    """
    munch = Meal.query \
    .join(Swipe)\
    .filter(Swipe.direction == 'right')\
    .filter(Meal.id == id)\
    .first()

    return munch

