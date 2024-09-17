from flask import Blueprint

privacy = Blueprint('privacy', __name__, template_folder='templates', static_folder='static')

from . import index
