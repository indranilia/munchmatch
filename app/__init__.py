from flask import Flask, redirect
from uuid import uuid4
from config import Config
from app.extensions import db, setFormatter, info_logger, error_logger
from app.models.user import User
from app.models.type import Type
from app.models.meal import Meal
from app.models.review import Review
from app.models.swipe import Swipe


def create_app(config_class=Config):
    """
    This function creates a Flask application instance and returns it.

    Parameters:
        config_class (Config): A configuration class to configure the Flask app
        instance. Defaults to `Config`, which comes from the configuration file
        that reads the environment variables.

    Returns:
        Flask: The Flask application instance.

    """
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config_class)

    # Initializing extensions
    fileFormatter = setFormatter(config_class.LOG_FILE_NAME)
    info_logger.addHandler(fileFormatter)
    error_logger.addHandler(fileFormatter)
    info_logger.info("File log for Tinder for Food opened")

    db.init_app(flaskApp)

    # Creating a function that will add types for food if it's empty
    def add_types():
        if not Type.query().first():
            italian = Type(uuid=str(uuid4()), name="Italian")
            db.session.add(italian)
            chinese = Type(uuid=str(uuid4()), name="Chinese")
            db.session.add(chinese)
            mexican = Type(uuid=str(uuid4()), name="Mexican")
            db.session.add(mexican)
            japanese = Type(uuid=str(uuid4()), name="Japanese")
            db.session.add(japanese)
            indian = Type(uuid=str(uuid4()), name="Indian")
            db.session.add(indian)
            american = Type(uuid=str(uuid4()), name="American")
            db.session.add(american)
            french = Type(uuid=str(uuid4()), name="French")
            db.session.add(french)
            thai = Type(uuid=str(uuid4()), name="Thai")
            db.session.add(thai)
            spanish = Type(uuid=str(uuid4()), name="Spanish")
            db.session.add(spanish)
            greek = Type(uuid=str(uuid4()), name="Greek")
            db.session.add(greek)
            korean = Type(uuid=str(uuid4()), name="Korean")
            db.session.add(korean)
            turkish = Type(uuid=str(uuid4()), name="Turkish")
            db.session.add(turkish)
            brazilian = Type(uuid=str(uuid4()), name="Brazilian")
            db.session.add(brazilian)
            other = Type(uuid=str(uuid4()), name="Other")
            db.session.add(other)
            db.session.commit()

    info_logger.info("DB Initiated")
    with flaskApp.app_context():
        db.create_all()
        info_logger.info("Tables created on DB")

    # Registering blueprints
    @flaskApp.errorhandler(404)
    def notFound(e):
        return redirect("/auth")

    from app.routes.auth import bp as auth_bp

    flaskApp.register_blueprint(auth_bp, url_prefix="/auth/")

    from app.routes.swipe import bp as swipe_bp

    flaskApp.register_blueprint(swipe_bp, url_prefix="/swipe/")

    return flaskApp
