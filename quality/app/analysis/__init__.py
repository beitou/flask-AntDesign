
from flask import Blueprint

analysis = Blueprint('analysis', __name__,
                    url_prefix='/api')

from app.analysis import views
