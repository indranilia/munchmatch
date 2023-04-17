from flask import Blueprint

bp = Blueprint('home', __name__)

from app.home import routes


#For the front-end, <link href='https://fonts.googleapis.com/css?family=Poppins' rel='stylesheet'> add this to the html head, 
# and use font-family: Poppins