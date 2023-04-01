import jwt

from flask import render_template, request, make_response, redirect, url_for
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta
from config import Config

from app.auth import bp
from app.models.user import User
from app.extensions import db, info_logger, error_logger
from app.integrations import emailSender
from config import Config


@bp.route('/login/', methods=['POST', 'GET'])
def login():
    """
    A route for logging in a user.

    GET requests will display the login page, while POST requests
    will attempt to log in the user.

    Returns:
        A rendered template containing the login page (for GET requests),
        or a response object indicating success or failure (for POST requests).
    """
    if (request.method == 'POST'):
        try:
            userData = request.get_json()

            existingUser = User.query\
                .filter_by(email=userData['email'])\
                .first()

            info_logger.info(
                f"Client tried to log in with email: {userData['email']}")

            if (not existingUser):
                error_logger.error(
                    f"User not found with email: {userData['email']}")
                return make_response({"message": 'User not found'}, 404)
            # Compares the password with the hashed password stored in the database
            elif (check_password_hash(existingUser.password, userData['password'])):
                if (existingUser.verified):
                    jwtToken = jwt.encode({
                        'uuid': existingUser.uuid,
                        'exp': datetime.utcnow() + timedelta(days=1)
                    }, Config.SECRET_KEY)

                    info_logger.info(
                        f"User successfully log in with email: {userData['email']}")

                    response = make_response(
                        {"message": 'User logged in!'}, 200)
                    response.set_cookie('user_uuid', jwtToken)

                    return response
                else:
                    error_logger.error(
                        f"User tried to log in with email: {userData['email']}, but they are not verified")
                    return make_response({"message": 'Please, verify your email first'}, 401)

            error_logger.error(
                f"User tried to log in with email: {userData['email']}, but used the wrong password")
            return make_response({"message": 'Wrong password'}, 401)
        except Exception as error:
            error_logger.error(f"Error on log in")
            return make_response({"message": error}, 500)
    else:
        if ('message' in request.args):
            info_logger.info(f"Login view rendered with message")
            response_auth = request.args['message']
            return render_template('./auth/login.html', message=response_auth)
        else:
            info_logger.info(f"Login view rendered without message")
            return render_template('./auth/login.html')


@bp.route('/register/', methods=['POST', 'GET'])
async def register():
    """
    A route for registering a new user.

    GET requests will display the registration page, while POST
    requests will attempt to create a new user.

    Returns:
        A rendered template containing the registration page (for GET
        requests), or a response object indicating success or failure
        (for POST requests).
    """
    if (request.method == 'POST'):
        try:
            newUserData = request.get_json()
            newUserData['uuid'] = str(uuid4())
            info_logger.info(
                f"Client tried to log in with email: {newUserData['email']}")

            existingUser = User.query\
                .filter_by(email=newUserData['email'])\
                .first()

            if (not existingUser):
                # Hashes the password for saving in the database
                newUserData['password'] = generate_password_hash(
                    newUserData['password'])
                user = User(**newUserData)
                db.session.add(user)
                db.session.commit()

                info_logger.info(
                    f"Email sent to {newUserData['email']} for user verify their account")

                # Sending verification email
                await emailSender.sendEmail(newUserData['email'], 'Verify your account for Kanban Board',
                                            'newUser', newUserData['firstName'],
                                            f"{request.url_root}auth/verify/{newUserData['uuid']}")

                info_logger.info(
                    f"User registered with email: {newUserData['email']}")

                return make_response({"message": 'User created successfully!\
                                      Enter your email to verify your account.\
                                      Remember to check your spam folder. (You may need\
                                      to mark as not a Span to access the link)'}, 201)
            else:
                info_logger.info(
                    f"User already registered with email: {newUserData['email']}")
                return make_response({"message": 'This email is already registered! Login now'}, 202)
        except Exception as error:
            error_logger.error(f"Error on registering")
            return make_response({"message": error}, 500)
    else:
        info_logger.info(f"Register view rendered")
        return render_template('./auth/register.html')


@bp.route('/logout/')
def logout():
    """
    A route for logging out a user.

    Returns:
        A response object indicating success.
    """
    info_logger.info(f"User logged out")
    response = make_response({"message": 'User logged out!'}, 200)
    response.set_cookie('user_uuid', expires=0)

    return response


@bp.route('/verify/<string:uuid>')
def verify(uuid):
    """
    A route for verifying a user's email.

    Returns:
        A response object indicating success.
    """
    try:
        existingUser = User.query\
            .filter_by(uuid=uuid)\
            .first()
        existingUser.verified = True
        info_logger.info(
            f"User verified with email: {existingUser.email}")
        db.session.commit()

        return (redirect(url_for('auth.login', message="User Verified!")))
    except Exception as error:
        error_logger.error(f"Error on verifying account")
        return (redirect(url_for('auth.login', message="Verification failed")))


@bp.route('/forgot-password/', methods=['POST', 'GET'])
async def forgotPassword():
    """
    A route for sending a forgot password email to a user.

    GET requests will display the forgot password page, while POST requests
    will attempt to send the email to the user.

    Returns:
        A rendered template containing the forgot password page (for GET requests),
        or a response object indicating success or failure (for POST requests).
    """
    if (request.method == 'POST'):
        try:
            userData = request.get_json()

            existingUser = User.query\
                .filter_by(email=userData['email'])\
                .first()

            info_logger.info(
                f"User forgot password with email: {existingUser.email}")

            if (not existingUser):
                info_logger.info(
                    f"User doesn't exist with email: {existingUser.email}")
                return make_response({"message": "User doesn't exist. Create your account first"}, 404)
            else:
                try:
                    info_logger.info(
                        f"Forgot password message sent to email: {existingUser.email}")
                    # Sending verification email
                    await emailSender.sendEmail(existingUser.email, 'Reset your Kanban Board password',
                                                'forgotPassword', existingUser.firstName,
                                                f"{request.url_root}auth/reset-password/{existingUser.uuid}")

                    return make_response({"message": f"Email sent to {existingUser.email}! Remember\
                                      to check your spam folder. (You may need to mark as not\
                                      a Span to access the link)"}, 200)
                except Exception as error:
                    error_logger.error(
                        f"Error on sending forgot password message to email: {existingUser.email}")
                    return make_response({"message": error}, 500)
        except Exception as error:
            error_logger.error(f"Error on forgot password")
            return make_response({"message": error}, 500)
    else:
        if ('message' in request.args):
            info_logger.info(
                f"Forgot Password view rendered with message")
            response_auth = request.args['message']
            return render_template('./auth/forgotPassword.html', message=response_auth)
        else:
            info_logger.info(
                f"Forgot Password view rendered without message")
            return render_template('./auth/forgotPassword.html')


@bp.route('/reset-password/<string:uuid>', methods=['GET', 'PATCH'])
def resetPassword(uuid):
    """
    A route for resetting a user's password.

    GET requests will display the reset password page, while POST requests
    will attempt to send the reset the user's password.

    Returns:
        A rendered template containing the reset password page (for GET requests),
        or a response object indicating success or failure (for POST requests).
    """
    if (request.method == 'PATCH'):
        try:
            userData = request.get_json()

            existingUser = User.query\
                .filter_by(uuid=uuid)\
                .first()

            info_logger.info(
                f"User reset password with email: {existingUser.email}")

            if (not existingUser):
                error_logger.error(
                    f"User not foung with email: {existingUser.email}")
                return make_response({"message": 'User not found'}, 404)
            else:
                existingUser.password = generate_password_hash(
                    userData['password'])
                db.session.commit()
                info_logger.info(
                    f"User successully resey password with email: {existingUser.email}")
                return make_response({"message": 'Password reset!'}, 204)

        except Exception as error:
            return make_response({"message": error}, 500)
    else:
        if ('message' in request.args):
            info_logger.info(
                f"Reset Password view rendered with message")
            response_auth = request.args['message']
            return render_template('./auth/resetPassword.html', message=response_auth)
        else:
            info_logger.info(
                f"Reset Password view rendered without message")
            return render_template('./auth/resetPassword.html')


@bp.errorhandler(404)
def notFound():
    return redirect('/auth/login')
