from flask import render_template
from . import help_page 

@help_page.route('/help')
def index():
    return render_template('help_page.html')
