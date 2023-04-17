from flask import Blueprint

bp = Blueprint('preferences', __name__)

from app.routes.munches import routes
