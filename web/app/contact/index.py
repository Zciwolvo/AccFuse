from flask import render_template
from . import contact

@contact.route('/contact')
def index():
    return render_template('contact_page.html')
