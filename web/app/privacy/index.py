from flask import render_template
from . import privacy 

@privacy.route('/privacy')
def index():
    return render_template('privacy.html')
