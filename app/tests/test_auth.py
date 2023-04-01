from app import create_app
from app.extensions import db
from app.models.user import User
import json
import unittest
import os

# Set up a test database
TEST_DB = 'test.db'
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
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, TEST_DB)
    LOG_FILE_NAME = 'log-test.txt'


class TestAuth(unittest.TestCase):
    """Test suite for the Kanban authentication routes"""

    def setUp(self):
        """Set up Kanban app, database, and test client"""
        self.flaskApp = create_app(TestConfig)
        self.app = self.flaskApp.test_client()

        with self.flaskApp.app_context():
            db.drop_all()
            db.create_all()

        self.assertEqual(self.flaskApp.debug, False)

    def tearDown(self):
        """Clean up after the test"""
        pass

    def register(self, name, gender, email, password):
        """
        Test helper function that sends a POST request to the '/auth/register' route.

        Args:
            name (str): The name of the user to register
            gender (int): The gender of the user to register
            email (str): The email address of the user to register
            password (str): The password of the user to register

        Returns:
            The response object of the POST request
        """
        return self.app.post(
            '/auth/register',
            data=json.dumps({"name": name, "gender": gender,
                             "email": email, "password": password}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def login(self, email, password):
        """
        Test helper function that sends a POST request to the '/auth/login' route.

        Args:
            email (str): The email address of the user to log in
            password (str): The password of the user to log in

        Returns:
            The response object of the POST request
        """
        return self.app.post(
            '/auth/login',
            data=json.dumps({"email": email, "password": password}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def verify(self, uuid):
        """
        Test helper function that sends a GET request to the '/auth/verify' route.

        Args:
            uuid (str): The uuid of the user

        Returns:
            The response object of the GET request
        """
        return self.app.get(
            f'/auth/verify/{uuid}',
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def test_auth(self):
        """
        Test the '/auth/register' and '/auth/login' routes.

        This method performs the following tests:
        - Test that the '/auth/register' and '/auth/login' routes return the correct status codes.
        - Test that registering a user with a unique email address works.
        - Test that registering a user with an already registered email address does not work.
        - Test that logging in before verifying doesn't work
        - Test that verifying works
        - Test that logging in after verifying works
        - Test that logging in with a valid email address and password works.
        - Test that logging in with an invalid password does not work.
        - Test that logging in with an unregistered email address does not work.
        """
        # Check if routes return 200
        response = self.app.get('/auth/register')
        self.assertEqual(response.status_code, 308)

        response = self.app.get('/auth/login')
        self.assertEqual(response.status_code, 308)

        # Check if registering works
        registerResponse = self.register(
            'TestName', 1, 'test@test.com', '123456')
        self.assertEqual(registerResponse.status_code, 201)

        # Getting user
        with self.flaskApp.app_context():
            newUser = User.query.one()

        # Check if registering doesn't work in case email is already registered
        registerResponse = self.register(
            'TestName', 1, 'test@test.com', '123456')
        self.assertEqual(registerResponse.status_code, 202)

        # Check if login doesn't work before verification
        loginResponse = self.login('test@test.com', '123456')
        self.assertEqual(loginResponse.status_code, 401)

        # Check if verification works
        verifyResponse = self.verify(newUser.uuid)
        self.assertEqual(verifyResponse.status_code, 200)

        # Check if login works after verification
        loginResponse = self.login('test@test.com', '123456')
        self.assertEqual(loginResponse.status_code, 200)

        # Check if login doesn't work with wrong password
        loginResponse = self.login('test@test.com', '12345')
        self.assertEqual(loginResponse.status_code, 401)

        # Check if login doesn't work with unexistent account
        loginResponse = self.login('test_unexistent@test.com', '123456')
        self.assertEqual(loginResponse.status_code, 404)
