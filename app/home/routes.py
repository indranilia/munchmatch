import jwt

from flask import render_template, request, make_response, redirect, url_for, session
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta
from config import Config

from app.auth import bp
from app.models.user import User
#import Meal as well
#import Swipe
from models.swipe import Swipe
from models.meal import Meal
from app.extensions import db, info_logger, error_logger
from app.integrations import emailSender
from config import Config
from sqlalchemy import func

@bp.route('/swipe/', methods=['GET', 'POST'])
def swipe_home():
    """
    A route for showing and handling swipe requests for meals

    GET method will display three random meals that are not in the swipe table yet
    POST method will handle swipes and add them to the swipe table

    Returns:
        A rendered template containing the swipe page with three random meals
    """
    # Get the user ID from the session
    user_id = session.get('user_id')

    if request.method == 'POST':
        # Get the meal ID and direction from the request
        meal_id = request.form.get('meal_id')
        direction = request.form.get('direction')

        # Add a new swipe to the database
        swipe = Swipe(uuid=str(uuid4()), direction=direction, user_id=user_id, meal_id=meal_id)
        db.session.add(swipe)
        db.session.commit()

        # Redirect to the previous page
        return redirect('./swipe.html')

    else:
        # Get three random meals that are not in the swipe table yet
        meals = Meal.query \
            .filter(Meal.id.notin_(db.session.query(Swipe.meal_id).filter_by(user_id=user_id))) \
            .limit(3) \
            .all()

        # Render the swipe template with the three meals
        return render_template('./swipe.html', meals=meals)


# @bp.route('/swipe/<int:meal_id>/swipe/<string:direction>', methods=['POST'])
# def swipe_meal(meal_id, direction):
#     """
#     A route for handling swipes of individual meals

#     Parameters:
#         meal_id (int): The ID of the meal being swiped
#         direction (int): The direction of the swipe (right=1 and left=0)

#     Returns:
#         A redirect to the previous swipe page
#     """
#     # Get the user ID from the session
#     user_id = session.get('user_id')

#     # Add a new swipe to the database
#     swipe = Swipe(id?, uuid=str(uuid4()), direction=direction, user_id=user_id, meal_id=meal_id)
#     swipe.session.add(swipe)
#     swipe.session.commit()

    # Redirect to the previous page
 #   return redirect(request.referrer)


