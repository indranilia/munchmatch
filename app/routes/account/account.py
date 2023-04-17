from flask import request, make_response
from app.extensions import db, info_logger, error_logger
from app.auth import bp
from app.models.user import User
from app.auth.routes import resetPassword
from werkzeug.exceptions import abort
from app.jwt import token_required

def get_user_info(id):
    currentUser = User.query\
        .filter_by(id=id)\
        .first()
    
    if currentUser is None:
        abort(404, f"User with id:{id} doesn't exist.")

    return currentUser

#add functionality to check if email is unique
@bp.route("/account/settings/change_email/", methods=["PATCH"])
@token_required
def change_email(uuid):
    try:
        reviewData = request.get_json()

        existingUser = User.query\
            .filter_by(uuid=uuid)\
            .first()
        
        info_logger.info(
            f"User email update")
        
        if not existingUser:
            error_logger.error(
                f"Email doesn't exist")
            return make_response({"message": 'Email not found'}, 404)
        else:
            existingUser.email = reviewData['email']
            db.session.commit()
            info_logger.info(
                f"Email was successully updated")
            return make_response({"message": 'Email update!'}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)

#add functionality to check if the username is unique
@bp.route("/account/settings/change_email/", methods=["PATCH"])
@token_required
def change_username(uuid):
    try:
        reviewData = request.get_json()

        existingUser = User.query\
            .filter_by(uuid=uuid)\
            .first()
        
        info_logger.info(
            f"Username update")
        
        if not existingUser:
            error_logger.error(
                f"Username doesn't exist")
            return make_response({"message": 'Username not found'}, 404)
        else:
            existingUser.username = reviewData['username']
            db.session.commit()
            info_logger.info(
                f"Username was successully updated")
            return make_response({"message": 'Username update!'}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)
    

@bp.route("/account/settings/name_update/", methods=["PATCH"])
@token_required
def change_name(uuid):
    try:
        reviewData = request.get_json()

        existingUser = User.query\
            .filter_by(uuid=uuid)\
            .first()
        
        info_logger.info(
            f"User's name update")
        
        if not existingUser:
            error_logger.error(
                f"User doesn't exist")
            return make_response({"message": 'User with given name not found'}, 404)
        else:
            existingUser.name = reviewData['name']
            db.session.commit()
            info_logger.info(
                f"User's name was successully updated")
            return make_response({"message": "User's name update!"}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)
    

@bp.route("/account/settings/change_picture/", methods=["PATCH"])
@token_required
def change_picture(uuid):
    try:
        reviewData = request.get_json()

        existingUser = User.query\
            .filter_by(uuid=uuid)\
            .first()
        
        info_logger.info(
            f"User's picture update")
        
        if not existingUser:
            error_logger.error(
                f"User doesn't exist")
            return make_response({"message": 'User with given name not found'}, 404)
        else:
            existingUser.name = reviewData['picture']
            db.session.commit()
            info_logger.info(
                f"User's picture was successully updated")
            return make_response({"message": "User's picture update!"}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)
    
@bp.route("/account/settings/change_password/", methods=["PATCH"])
@token_required
def change_password(uuid):
    resetPassword(uuid)