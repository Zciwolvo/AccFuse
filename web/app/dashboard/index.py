from flask import render_template, session, current_app as app
from . import dashboard
from ..database.Models import Account
from flask_jwt_extended import get_jwt_identity, jwt_required

@dashboard.route('/dashboard')
@jwt_required()
def index():
    user_id = get_jwt_identity()
    with app.app_context():
        has_accounts = Account.query.filter_by(user_id=user_id).first() is not None

    return render_template('dashboard.html', has_accounts=has_accounts)
