from flask import render_template, request, make_response, redirect, url_for
from uuid import uuid4
from datetime import datetime
from app.extensions import db, info_logger, error_logger
from app.auth import bp
from app.models.meal import Meal
from app.models.review import Review
from werkzeug.exceptions import abort
from auth import token_required


class Swipe(db.Model):
    """
    A class representing a swipe in the tinder for food app.

    Attributes:
        id (int): The unique identifier for the swipe.
        uuid (str): A Universally Unique Identifier (UUID) for the swipe.
        direction (int): The direction of the swipe (left = 0 / right = 1).
        user_id (int): The ID of the user who swiped.
        meal_id (int): The ID of the meal that was swiped.
        all_swipes(list): All of the swipes a user currently has

    Methods:
        __repr__(): Returns a string representation of the Swipe object.
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    direction = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    all_swipes = []

    def __repr__(self):
        """
        Returns a string representation of the Swipe object.

        Returns:
            str: A string representation of the Swipe object, including the swipe uuid.
        """
        return f'<Swipe "{self.uuid}">'
    
    def get_random_meal(self):

        currentMeal = Meal.query\
        .first()

        if currentMeal.meal_id in self.all_swipes:
            self.get_random_meal()

        return currentMeal
    
    def swipe(self):
        if self.direction == 1:
            self.all_swipes.append(self.meal_id)
    

