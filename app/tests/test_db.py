from app import create_app
from app.extensions import db
from app.models.user import User
import app
import json
import unittest
import os
import uuid

# Set up a test database
TEST_DB = "test.db"
basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig:
    """
    Testing Configuration settings for the Flask app.
    Attributes:
    - TESTING: Testing state
    - WTF_CSRF_ENABLED: Whether CSRF protection is enabled
    - DEBUG: Debug mode
    - SQLALCHEMY_DATABASE_URI: the connection URI for the database
    - LOG_FILE_NAME: Log file name
    """

    TESTING = True
    WTF_CSRF_ENABLED = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ("sqlite:///" + os.path.join(basedir, TEST_DB) + "?timeout=20")
    LOG_FILE_NAME = "log-test.txt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    


user = User(id = 1, uuid = str(uuid.uuid4()), name ='Jessica', 
            email ='jessica@gmail.com', password ='password')

class TestUser(unittest.TestCase):
    """Test suite for the authentication routes"""

    def setUp(self):
        """Set up app, database, and test client"""
        self.flaskApp = create_app(TestConfig)
        self.app = self.flaskApp.test_client()

        with self.flaskApp.app_context():
            db.drop_all()
            db.create_all()
        self.assertEqual(self.flaskApp.debug, False)


    def test_correct_account(self):
         with self.flaskApp.app_context():
             db.session.add(user)
             result = db.session.query(User).filter(User.id == 1).first()
         self.assertEqual(result, user)
        
    def test_wrong_account(self):
        with self.flaskApp.app_context():
            db.session.add(user)
            result = db.session.query(User).filter(User.id == 2).first()
        self.assertNotEqual(result, user)
    
    def test_email_query_right(self):
        with self.flaskApp.app_context():
            db.session.add(user)
            result = db.session.query(User).filter(User.email == 'jessica@gmail.com').first()
        self.assertEqual(result, user)
    
    def test_email_query_wrong(self):
        with self.flaskApp.app_context():
            db.session.add(user)
            result = db.session.query(User).filter(User.email == "annie@gmail.com").first()
        self.assertNotEqual(result, user)
    
    def text_email_update(self):
        with self.flaskApp.app_context():
            db.session.add(user)
            db.session.update(User).filter(User.email == "newemail@gmail.com").where(User.id == 1)
            result = db.session.query(User).filter(User.id == 1).first()
        self.assertNotEqual(result, "jessica@gmail.com")
        self.assertEqual(result, "newemail@gmail.com")
    
    def text_name_update(self):
        with self.flaskApp.app_context():
            db.session.add(user)
            db.session.update(User).filter(User.name == "Jess").where(User.id == 1)
            result = db.session.query(User).filter(User.id == 1).first()
        self.assertNotEqual(result, "Jessica")
        self.assertEqual(result, "Jess")

    def tearDown(self):
        """Clean up after the test"""
        pass
