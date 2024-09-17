from flask import Blueprint

contact = Blueprint('contact', __name__, template_folder='templates', static_folder='static')

from . import index
