from flask import Blueprint

bp = Blueprint('preferences', __name__)

from app.preferences import preferences
