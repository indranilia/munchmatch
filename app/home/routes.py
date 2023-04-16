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

#remove and add new


@bp.route('/preferences/', methods=['POST', 'GET'])
async def preferences():
    """
    A route for preferences
    """
    return render_template('./preferences/prefhome.html')

