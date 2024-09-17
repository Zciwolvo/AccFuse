from flask import Blueprint

help_page = Blueprint('help_page', __name__, template_folder='templates', static_folder='static')

from . import index
