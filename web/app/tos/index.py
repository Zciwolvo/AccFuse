from flask import render_template
from . import tos 

@tos.route('/tos')
def index():
    return render_template('tos.html')
