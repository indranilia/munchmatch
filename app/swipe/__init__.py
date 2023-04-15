from flask import Blueprint

bp = Blueprint("swipe", __name__)

from app.swipe import routes
