from app.extensions import db

class Preferences(db.Model):
    """
    A class representing a meal in the tinder for food app.

    Attributes:

    Methods:
        __repr__(): Returns a string representation of the Meal object.
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    location = db.Column(db.String(150))
    range = db.Column(db.Float)
    diet = db.Column(db.String(150))
    cuisine = db.Column(db.String(150))

    def __repr__(self):
        """
        Returns a string representation of the Meal object.

        Returns:
            str: A string representation of the Meal object, including the Meal name.
        """
        return f'<Meal "{self.name}">'
