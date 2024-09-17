from flask import Blueprint

tos = Blueprint('tos', __name__, template_folder='templates', static_folder='static')

from . import index
