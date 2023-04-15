from flask import render_template, request, make_response, redirect, url_for
from uuid import uuid4
from datetime import datetime
from app.extensions import db, info_logger, error_logger
from app.auth import bp
from app.models.meal import Meal
from app.models.review import Review
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

            existingReview = Review.query\
                .filter_by(user_id=newData['user_id'], meal_id=newData['meal_id'])\
                .first()
            
            if not existingReview:
                review = Review(**newReview)
                db.session.add(review)
                db.session.commit()
        except Exception as error:
            error_logger.error(f"Error on adding review")
            return make_response({"message": error}, 500)
    else:
        info_logger.info(f"Preferences view rendered")
        return render_template('./preferences.html')   
    