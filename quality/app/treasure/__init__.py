
from flask import Blueprint

treasure = Blueprint('treasure', __name__,
                     url_prefix='/api')

from app.treasure import views
