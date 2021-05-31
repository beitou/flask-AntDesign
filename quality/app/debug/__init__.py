
from flask import Blueprint

debug = Blueprint('debug', __name__,
                    url_prefix='/api')

from app.debug import views
