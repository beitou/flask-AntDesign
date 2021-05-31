
from flask import Blueprint

genesis = Blueprint('genesis', __name__,
                    url_prefix='/api')

from app.genesis import views
