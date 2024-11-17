from flask import render_template, session, current_app as app, redirect, request, jsonify, url_for
from . import dashboard
from ..database.Models.Account import Account
from flask_jwt_extended import get_jwt_identity, jwt_required
from .BankController import BANK_CONFIGURATIONS, initialize_bank_api, authenticate_user, combine_data

@dashboard.route('/dashboard')
@jwt_required()
def index():
    user_id = get_jwt_identity()
    with app.app_context():
        has_accounts = Account.query.filter_by(user_id=user_id).first() is not None

    return render_template('dashboard.html', has_accounts=has_accounts)

@dashboard.route('/connect_bank')
def connect_bank():
    return render_template('connect_bank.html')

def fetch_data(bank, username, password):
    """
    Main route that processes all steps: authentication, fetching IBANs, 
    and retrieving transaction and balance data.
    """

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Step 1: Initialize BankAPI
    bank_api, error = initialize_bank_api(bank)
    if error:
        return error

    # Step 2: Authenticate user
    access_token, error = authenticate_user(bank_api, username, password)
    if error:
        return error

    # Step 3: Fetch transaction and balance data
    data, error = combine_data(bank_api, access_token)
    if error:
        return error

    return jsonify(data)


@dashboard.route('/bank_login/<bank>', methods=['GET', 'POST'])
def bank_login(bank):
    """Renders login page or processes user login."""
    bank_config = BANK_CONFIGURATIONS.get(bank)
    if not bank_config:
        return "Invalid bank selected", 400

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Initialize BankAPI
        bank_api, error = initialize_bank_api(bank)
        if error:
            return error

        # Authenticate user and fetch IBANs
        access_token, error = authenticate_user(bank_api, username, password)
        if error:
            return error

        # Generate authorization URL
        ibans = bank_api.get_ibans(access_token)
        authorization_code = bank_api.get_authorization_code(access_token, ibans)
        authoriztion_url = f"{bank_config['auth_base_url']}/cardsAuthorizeConfirm?code={authorization_code}&redirectTo={bank_config["redirect_uri"]}&state=api&appName=AccFuse&cards=N"

        # Redirect user to bank's authorization page
        return redirect(authoriztion_url)

    return render_template('bank_login.html', bank_name=bank.capitalize(), bank=bank)


@dashboard.route('/dashboard/redirect', methods=['GET'])
def handle_redirect():
    """Handle redirect from the bank after authorization."""
    authorization_code = request.args.get('code')
    state = request.args.get('state')  # Bank identifier
    if not authorization_code or not state:
        return "Authorization failed", 400

    # Initialize BankAPI
    bank_api, error = initialize_bank_api(state)
    if error:
        return error

    # Exchange authorization code for a new access token
    new_access_token = bank_api.get_new_access_token(authorization_code)
    if not new_access_token:
        return "Failed to exchange authorization code", 400

    # Fetch and save account data
    account_data = bank_api.get_account_data(new_access_token)
    ibans = bank_api.get_ibans(new_access_token)
    transactions = []
    balances = []

    for iban in ibans:
        transactions.append(bank_api.get_transaction_data(iban, new_access_token))
        balances.append(bank_api.get_balance_data(iban, new_access_token))

    # Save data to database (Example)
    #user_id = get_jwt_identity()
    #save_to_database(user_id, state, account_data, transactions, balances)

    return redirect(url_for('dashboard.index'))  # Redirect back to dashboard