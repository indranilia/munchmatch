from flask import render_template, request, make_response, redirect, url_for
from uuid import uuid4
from datetime import datetime
from app.extensions import db, info_logger, error_logger
from app.auth import bp
from app.models.preferences import Preferences
from werkzeug.exceptions import abort
from app.jwt import token_required


@bp.route("/add_preferences/", methods=["GET", "POST"])
@token_required
def add_review():
    """
    Adding a review
    Parameters
    -----------
    
    Returns
    -----------
    Added review
    """
    if request.method == "POST":
        try:

            newData = request.get_json()
            newData['uuid'] = str(uuid4())

            existingReview = Preferences.query\
                .filter_by(user_id=newData['user_id'], meal_id=newData['meal_id'])\
                .first()
            
            if not existingReview:
                preference = Preferences(**newReview)
                db.session.add(preference)
                db.session.commit()
        except Exception as error:
            error_logger.error(f"Error on adding preference")
            return make_response({"message": error}, 500)
    else:
        info_logger.info(f"Preferences view rendered")
        return render_template('./preferences.html')   

@bp.route("/account/settings/range_update/", methods=["PATCH"])
@token_required
def change_range(uuid):
    try:
        reviewData = request.get_json()

        existingUser = Preferences.query\
            .filter_by(uuid=uuid)\
            .first()
        
        info_logger.info(
            f"Range update")
        

        existingUser.range = reviewData['range']
        db.session.commit()
        info_logger.info(
            f"Range was successully updated")
        return make_response({"message": "Range update!"}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)

@bp.route("/account/settings/diet_update/", methods=["PATCH"])
@token_required
def change_diet(uuid):
    try:
        reviewData = request.get_json()

        existingUser = Preferences.query\
            .filter_by(uuid=uuid)\
            .first()
        
        info_logger.info(
            f"Diet update")
        

        existingUser.diet = reviewData['diet']
        db.session.commit()
        info_logger.info(
            f"Diet was successully updated")
        return make_response({"message": "Diet update!"}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)
    
@bp.route("/account/settings/cuisine_update/", methods=["PATCH"])
@token_required
def change_cuisine(uuid):
    try:
        reviewData = request.get_json()

        existingUser = Preferences.query\
            .filter_by(uuid=uuid)\
            .first()
        
        info_logger.info(
            f"Cuisine update")
        

        existingUser.cuisine = reviewData['cuisine']
        db.session.commit()
        info_logger.info(
            f"Cuisine was successully updated")
        return make_response({"message": "Cuisine update!"}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)
    