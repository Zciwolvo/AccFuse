from flask import Blueprint, request, jsonify, render_template, redirect, url_for
import uuid
from .BankAPI import BankAPI  # Ensure BankAPI is imported correctly

account = Blueprint('account', __name__)

BANK_CONFIGURATIONS = {
    'bnp_paribas': {
        'client_id': 'faadd989-102d-4ba1-b9fd-c01d45c75849',
        'client_secret': '6270e8b2f3a78b447271e02c67e7a37e7ae52d7a86f137335c6ec825bdba3ecc5c55b33ba132db8e97215aeca0046ee2',
        'auth_base_url': 'https://sandbox.auth.bnpparibasfortis.com',
        'api_base_url': 'https://sandbox.api.bnpparibasfortis.com/psd2/v3',
        'redirect_uri': 'http://localhost:5000/dashboard/redirect',
        'brand': 'bnppf',
    },
    'fintro': {
        'client_id': 'faadd989-102d-4ba1-b9fd-c01d45c75849',
        'client_secret': '6270e8b2f3a78b447271e02c67e7a37e7ae52d7a86f137335c6ec825bdba3ecc5c55b33ba132db8e97215aeca0046ee2',
        'auth_base_url': 'https://sandbox.auth.bnpparibasfortis.com',
        'api_base_url': 'https://sandbox.api.bnpparibasfortis.com/psd2/v3',
        'redirect_uri': 'http://localhost:5000/dashboard/redirect',
        'brand': 'fintro',
    },
    'hellobank': {
        'client_id': 'faadd989-102d-4ba1-b9fd-c01d45c75849',
        'client_secret': '6270e8b2f3a78b447271e02c67e7a37e7ae52d7a86f137335c6ec825bdba3ecc5c55b33ba132db8e97215aeca0046ee2',
        'auth_base_url': 'https://sandbox.auth.bnpparibasfortis.com',
        'api_base_url': 'https://sandbox.api.bnpparibasfortis.com/psd2/v3',
        'redirect_uri': 'http://localhost:5000/dashboard/redirect',
        'brand': 'hb',
    },
}


def initialize_bank_api(bank):
    """Initialize BankAPI instance for the given bank."""
    bank_config = BANK_CONFIGURATIONS.get(bank)
    if not bank_config:
        return None, jsonify({"error": "Invalid bank selected"}), 400
    return BankAPI(bank_config), None


def authenticate_user(bank_api, username, password):
    """Authenticate the user and return an access token."""
    access_token = bank_api.get_access_token(username, password)
    if not access_token:
        return None, jsonify({"error": "Authentication failed"}), 400
    return access_token, None


def fetch_data(bank_api, access_token):
    """Fetch transaction and balance data."""
    ibans = bank_api.get_ibans(access_token)
    if not ibans:
        return None, jsonify({"error": "Failed to retrieve IBANs"}), 400
    account_data = bank_api.get_account_data(access_token)
    data = {
        "account": account_data,
        "transactions": [],
        "balances": [],
    }

    for iban in ibans:
        transaction_data = bank_api.get_transaction_data(iban, access_token)
        balance_data = bank_api.get_balance_data(iban, access_token)
        if transaction_data:
            data["transactions"].append(transaction_data)
        if balance_data:
            data["balances"].append(balance_data)

    return data, None


@account.route('/process/<bank>', methods=['POST'])
def process_bank_data(bank):
    """
    Main route that processes all steps: authentication, fetching IBANs, 
    and retrieving transaction and balance data.
    """
    username = request.json.get('username')
    password = request.json.get('password')

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
    data, error = fetch_data(bank_api, access_token)
    if error:
        return error

    return jsonify(data)


@account.route('/login/<bank>', methods=['GET', 'POST'])
def login(bank):
    """Renders login page or processes user login."""
    bank_config = BANK_CONFIGURATIONS.get(bank)
    if not bank_config:
        return "Invalid bank selected", 400

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        return redirect(
            url_for('account.process_bank_data', bank=bank, username=username, password=password)
        )

    return render_template('login.html', bank_name=bank.capitalize(), bank=bank)
