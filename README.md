# Tinder for Food 12:30

## Project Structure

`/.github/workflows` contains CI/CD code.

`/app` contains the application.

`/app/static` contains css/img/js files.

`/app/templates` contains html files.

`/app/__init__.py` is the project initializer file.

`/app/auth` contains the routes related to authentication.

`/app/models` contains the DB models using SQLAlchemy.

`/app/integrations` contains third-party integrations.

`/app/extensions.py` contains build-in extensions that are initialized in `__init__.py`.

`/app/jwt.py` contains the code for JWT authentication.

`/app/tests` contains the unit tests files.

`/.env.example` contains the variables you need for your .env.

`/config.py` contains the environment variables used in this code

## Before you start

The `.env.example` contains all the environment variables you need to run this program. Simply copy all the content from it and paste in a new file called `.env` in the root of the app (same level as the app folder and the `.env.example` file).

## Virtual Environment and run the app
Create the virtualenv:

    $ virtualenv -p python3 venv

Sometimes, the above doesn't work. You can try then:

    $ python3 -m venv venv

Then, activate the activate the virtualenv. For Mac

    $ source venv/bin/activate

For **Windows** - [reference source:](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

    $ venv\Scripts\activate

Install dependencies in virtual environment:

    $ pip3 install -r requirements.txt

To set the FLASK_APP varibale:

    $ export FLASK_APP=app

To start the server:

	$ python3 -m flask run

To run the unit tests:

	$ python3 -m unittest discovery app/tests

When you are done. Close the virtual env.

    $ deactivate