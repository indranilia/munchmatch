from flask import request, make_response
from uuid import uuid4
from app.extensions import db, error_logger
from app.routes.auth import bp
from app.models.meal import Meal
from app.jwt import token_required

@bp.route("/add_meal/", methods=["POST"])
@token_required
def add_meal():
    """
    Adding a meal
    Parameters
    -----------
    
    Returns
    -----------
    Added meal
    """
    try:

        newMeal = request.get_json()
        newMeal['uuid'] = str(uuid4())

        existingMeal = Meal.query\
            .filter_by(id=newMeal['id'])\
            .first()
        
        if not existingMeal:
            meal = Meal(**newMeal)
            db.session.add(meal)
            db.session.commit()
    except Exception as error:
        error_logger.error(f"Error on adding a meal")
        return make_response({"message": error}, 500)