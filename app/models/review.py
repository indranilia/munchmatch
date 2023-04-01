from app.extensions import db


class Review(db.Model):
    """
    A class representing a review in the tinder for food app.

    Attributes:
        id (int): The unique identifier for the review.
        uuid (str): A Universally Unique Identifier (UUID) for the review.
        rating (int): The review's rating.
        user_id (int): The ID of the user who added the review.

    Methods:
        __repr__(): Returns a string representation of the Review object.
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """
        Returns a string representation of the Review object.

        Returns:
            str: A string representation of the Review object, including the review uuid.
        """
        return f'<Review "{self.uuid}">'
