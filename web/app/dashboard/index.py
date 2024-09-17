from flask import render_template
from . import dashboard 

@dashboard.route('/dashboard')
def index():
    return render_template('dashboard.html')

