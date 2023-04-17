from flask import request, render_template, make_response, redirect
from app.extensions import db, info_logger, error_logger
from app.auth import bp
from app.models.user import User
from app.auth.routes import resetPassword
from werkzeug.security import generate_password_hash, check_password_hash
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

        existingEmail = User.query\
            .filter_by(email=reviewData['email'])\
            .first()
                
        info_logger.info(
            f"User email update")
        
        if not existingUser:
            error_logger.error(
                f"User doesn't exist")
            return make_response({"message": 'Email not found'}, 404)
        
        elif existingEmail:
            error_logger.error(
                f"User with given email already exist")
            return make_response({"message": 'Existing email'}, 404)
            
        else:
            existingUser.email = reviewData['email']
            db.session.commit()
            info_logger.info(
                f"Email was successully updated")
            return make_response({"message": 'Email update!'}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)

#add functionality to check if the username is unique
@bp.route("/account/settings/change_username/", methods=["PATCH"])
@token_required
def change_username(uuid):
    try:
        reviewData = request.get_json()

        existingUser = User.query\
            .filter_by(uuid=uuid)\
            .first()
        
        existingUsername = User.query\
            .filter_by(email=reviewData['username'])\
            .first()
        
        info_logger.info(
            f"Username update")
        
        if not existingUser:
            error_logger.error(
                f"Username doesn't exist")
            return make_response({"message": 'Username not found'}, 404)
        
        elif existingUsername == existingUser.username:
            error_logger.error(
                f"You are logged in with a current username")
            return make_response({"message": 'Username exists'}, 404)

        elif existingUsername:
            error_logger.error(
                f"User with given username already exist")
            return make_response({"message": 'Username already exists'}, 404)

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
            return make_response({"message": "Name update"}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)
    

@bp.route("/account/settings/change_picture/", methods=["PATCH"])
@token_required
def change_picture(uuid):
    try:
        reviewData = request.get_json()#imagine it's url
        #need to clarify how to import the images 

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
            #assuming picture is in USER table
            existingUser.picture = reviewData['picture']
            db.session.commit()
            info_logger.info(
                f"User's picture was successully updated")
            return make_response({"message": "User's picture update!"}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)
    
@token_required
@bp.route("/account/settings/change_password/", methods=['POST', 'GET'])
def change_password(uuid):

    if (request.method == 'POST'):
        try:
            userData = request.get_json()

            existingUser = User.query\
                .filter_by(uuid=uuid)\
                .first()

            info_logger.info(
                f"Client tried to change password associated with email: {userData['email']}")

            if (not existingUser):
                error_logger.error(
                    f"User not found with email: {userData['email']}")
                return make_response({"message": 'User not found'}, 404)
            # Compares the password with the hashed password stored in the database
            elif (check_password_hash(existingUser.password, userData['password'])):
                if (existingUser.verified):

                    info_logger.info(
                        f"Correct password for: {userData['email']}")
                    
                    existingUser.password = generate_password_hash(userData['new_password'])
                    db.session.commit()
                    info_logger.info(
                        f"User successully reset password with email: {existingUser.email}")
                    return make_response({"message": 'Password reset!'}, 204)

                else:
                    error_logger.error(
                        f"User tried to log in with email: {userData['email']}, but they are not verified")
                    return make_response({"message": 'Please, verify your email first'}, 401)

            error_logger.error(
                f"User tried to change password for email: {userData['email']}, but used the wrong password")
            return make_response({"message": 'Wrong password'}, 401)
        except Exception as error:
            error_logger.error(f"Error on verification")
            return make_response({"message": error}, 500)
    else:
        if ('message' in request.args):
            info_logger.info(f"Account settings view rendered with message")
            response_auth = request.args['message']
            return render_template('./account/settings.html', message=response_auth)
        else:
            info_logger.info(f"Account settings view rendered without message")
            return render_template('./account/settings.html')

@bp.errorhandler(404)
def notFound():
    return redirect('/account/settings')