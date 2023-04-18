from flask import render_template, request, make_response, jsonify
from uuid import uuid4
from app.extensions import db, info_logger, error_logger
from app.routes.preferences import bp
from app.models.preferences import Preferences
from app.models.preferences_type import preferences_type
from app.models.type import Type
from app.jwt import token_required


@bp.route("/")
@token_required
def preferences(user):
    """
    A route for preferences
    """
    types = Type.query.all()
    return render_template("./preferences/prefhome.html", types=types)


@bp.route("/get_preferences/")
@token_required
def get_preferences(user):
    """
    A route for preferences
    """
    try:
        query = Preferences.query.filter(Preferences.user_id == user.id).first()

        preferencesCuisineRelation = (
            db.session.query(preferences_type).filter_by(preferences_id=query.id).all()
        )

        preferencesCuisine = [
            Type.query.filter(Type.id == relation.type_id).first()
            for relation in preferencesCuisineRelation
        ]

        existingPreferences = query.as_dict()
        existingPreferences["cuisine"] = [
            cuisine.as_dict() for cuisine in preferencesCuisine
        ]

        return make_response(
            {
                "message": "Preferences retrieved successfully",
                "preferences": existingPreferences,
            },
            200,
        )
    except Exception as error:
        error_logger.error(f"Error on getting preference")
        return make_response({"message": error}, 500)


@bp.route("/update_preferences/", methods=["POST"])
@token_required
def update_preferences(user):
    """
    Adding a review
    Parameters
    -----------

    Returns
    -----------
    Added preferences
    """
    try:
        newData = request.get_json()

        existingPreference = Preferences.query.filter_by(user_id=user.id).first()
        existingPreference.range = newData["range"]
        existingPreference.location = newData["location"]

        db.session.commit()
        return make_response(
            {
                "message": "Preference updated successfully",
            },
            200,
        )
    except Exception as error:
        error_logger.error(f"Error on adding preference")
        return make_response({"message": error}, 500)


@bp.route("/add_preferences_type/", methods=["POST"])
@token_required
def add_preferences_type(user):
    """
    Adding a review
    Parameters
    -----------

    Returns
    -----------
    Added preferences
    """
    try:
        newData = request.get_json()

        existingPreference = Preferences.query.filter_by(user_id=user.id).first()

        newCuisine = {}
        for cuisine in newData["cuisine"]:
            if "name" not in cuisine:
                newCuisine = cuisine

        newData["cuisine"] = [
            Type.query.filter_by(uuid=cuisine["uuid"]).first()
            for cuisine in newData["cuisine"]
        ]

        for cuisine in newData["cuisine"]:
            if newCuisine["uuid"] == cuisine.uuid:
                newCuisine = cuisine
        db.session.execute(
            preferences_type.insert(),
            params={"preferences_id": existingPreference.id, "type_id": newCuisine.id},
        )

        db.session.commit()
        return make_response(
            {
                "message": "Preference type added successfully",
            },
            200,
        )
    except Exception as error:
        error_logger.error(f"Error on adding preference")
        return make_response({"message": error}, 500)


@bp.route("/remove_preferences_type/", methods=["POST"])
@token_required
def remove_preferences_type(user):
    """
    Adding a review
    Parameters
    -----------

    Returns
    -----------
    Added preferences
    """
    try:
        newData = request.get_json()

        existingPreference = Preferences.query.filter_by(user_id=user.id).first()
        correspondingType = Type.query.filter_by(uuid=newData["uuid"]).first()

        db.session.query(preferences_type).filter_by(
            preferences_id=existingPreference.id, type_id=correspondingType.id
        ).delete()

        db.session.commit()

        return make_response(
            {
                "message": "Preferences type deleted successfully",
            },
            200,
        )
    except Exception as error:
        error_logger.error(f"Error on adding preference")
        return make_response({"message": error}, 500)