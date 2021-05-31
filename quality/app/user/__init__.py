
from flask import Blueprint

user = Blueprint('user', __name__, url_prefix='/api')

from app.user import views
