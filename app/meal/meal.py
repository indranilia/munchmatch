from flask import render_template, request, make_response, redirect, url_for
from uuid import uuid4
from datetime import datetime
from app.extensions import db, info_logger, error_logger
from app.auth import bp
from app.models.meal import Meal
from app.models.review import Review
from werkzeug.exceptions import abort
from app.jwt import token_required





@bp.route("/meal/<int:id>/", methods=["GET", "POST"])
@token_required
def get_meal(id):

    currentMeal = Meal.query\
        .filter_by(id=id)\
        .first()
    
    if currentMeal is None:
        abort(404, f"Meal with id:{id} doesn't exist.")

    return currentMeal



@bp.route("/add_review/", methods=["GET", "POST"])
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

            newReview = request.get_json()
            newReview['uuid'] = str(uuid4())

            existingReview = Review.query\
                .filter_by(user_id=newReview['user_id'], meal_id=newReview['meal_id'])\
                .first()
            
            if not existingReview:
                review = Review(**newReview)
                db.session.add(review)
                db.session.commit()
        except Exception as error:
            error_logger.error(f"Error on adding review")
            return make_response({"message": error}, 500)
    else:
        info_logger.info(f"Review view rendered")
        return render_template('./meal/reviews.html')   
    
@bp.route("/update_review/<string:uuid>", methods=["GET", "PATCH"])
@token_required
def update_review(uuid):
    if request.method == 'PATCH':
        try:
            reviewData = request.get_json()

            existingReview = Review.query\
                .filter_by(uuid=uuid)\
                .first()
            
            info_logger.info(
                f"User review update")
            
            if not existingReview:
                error_logger.error(
                    f"Review doesn't exist")
                return make_response({"message": 'Review not found'}, 404)
            else:
                existingReview.description = reviewData['description']
                existingReview.rating = reviewData['rating']
                existingReview.date = datetime.utcnow()
                db.session.commit()
                info_logger.info(
                    f"Review was successully updated")
                return make_response({"message": 'Review update!'}, 204)

        except Exception as error:
            return make_response({"message": error}, 500)
            

@bp.route("/update_review/<string:uuid>", methods=["GET", "PATCH"])
@token_required
def update_review(uuid):
    if request.method == 'PATCH':
        try:
            reviewData = request.get_json()

            existingReview = Review.query\
                .filter_by(uuid=uuid)\
                .first()
            
            info_logger.info(
                f"User review update")
            
            if not existingReview:
                error_logger.error(
                    f"Review doesn't exist")
                return make_response({"message": 'Review not found'}, 404)
            else:
                existingReview.description = reviewData['description']
                existingReview.rating = reviewData['rating']
                existingReview.date = datetime.utcnow()
                db.session.commit()
                info_logger.info(
                    f"Review was successully updated")
                return make_response({"message": 'Review update!'}, 204)

        except Exception as error:
            return make_response({"message": error}, 500)
    else:
        info_logger.info(f"Review updated")
        return render_template('./meal/reviews.html')
            

@bp.route("/delete/<int:id>", methods=["POST"])
@token_required
def delete(uuid):
    """
    Delete a review
    Parameters
    -----------
    uuid (str): A Universally Unique Identifier (UUID) for the review.
    
    Returns
    -----------
    
    """
    try:
        existingReview = Review.query\
            .filter_by(uuid=uuid)\
            .first()
                
        info_logger.info(
            f"Deleting user review")
                
        if not existingReview:
            error_logger.error(
                f"Review doesn't exist")
            return make_response({"message": 'Review not found'}, 404)
        else:
            db.session.delete(existingReview)
            db.session.commit()
            info_logger.info(
                f"Review was successully deleted")
            return make_response({"message": 'Review deleted!'}, 204)
    except Exception as error:
        return make_response({"message": error}, 500)
            