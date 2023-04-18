from flask import request, render_template, make_response, redirect
from app.extensions import db, info_logger, error_logger
from app.routes.account import bp
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import abort
from app.jwt import token_required


@bp.route("/")
@token_required
def get_account(user):
    return render_template("/account/account.html", user=user)


# add functionality to check if email is unique
@bp.route("/", methods=["PATCH"])
@token_required
def change_values(user):
    try:
        reviewData = request.get_json()

        existingUser = User.query.filter_by(uuid=user.uuid).first()

        existingEmail = User.query.filter_by(email=reviewData["email"]).first()

        info_logger.info(f"User email update")

        if existingEmail and existingUser.email != existingEmail.email:
            error_logger.error(f"User with given email already exist")
            return make_response({"message": "Existing email"}, 500)

        existingUser.email = reviewData["email"]
        existingUser.name = reviewData["name"]

        db.session.commit()
        info_logger.info(f"Account updated successfully!")
        return make_response({"message": "Account updated successfully!"}, 204)

    except Exception as error:
        return make_response({"message": error}, 500)
