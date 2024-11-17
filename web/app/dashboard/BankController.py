from .BankAPI import BankAPI  # Ensure BankAPI is imported correctly

BANK_CONFIGURATIONS = {
    'bnp_paribas': {
        'client_id': 'faadd989-102d-4ba1-b9fd-c01d45c75849',
        'client_secret': '6270e8b2f3a78b447271e02c67e7a37e7ae52d7a86f137335c6ec825bdba3ecc5c55b33ba132db8e97215aeca0046ee2',
        'auth_base_url': 'https://sandbox.auth.bnpparibasfortis.com',
        'api_base_url': 'https://sandbox.api.bnpparibasfortis.com/psd2/v3',
        'redirect_uri': 'http://www.localhost:5000/dashboard/redirect',
        'brand': 'bnppf',
    },
    'fintro': {
        'client_id': 'faadd989-102d-4ba1-b9fd-c01d45c75849',
        'client_secret': '6270e8b2f3a78b447271e02c67e7a37e7ae52d7a86f137335c6ec825bdba3ecc5c55b33ba132db8e97215aeca0046ee2',
        'auth_base_url': 'https://sandbox.auth.bnpparibasfortis.com',
        'api_base_url': 'https://sandbox.api.bnpparibasfortis.com/psd2/v3',
        'redirect_uri': 'http://www.localhost:5000/dashboard/redirect',
        'brand': 'fintro',
    },
    'hellobank': {
        'client_id': 'faadd989-102d-4ba1-b9fd-c01d45c75849',
        'client_secret': '6270e8b2f3a78b447271e02c67e7a37e7ae52d7a86f137335c6ec825bdba3ecc5c55b33ba132db8e97215aeca0046ee2',
        'auth_base_url': 'https://sandbox.auth.bnpparibasfortis.com',
        'api_base_url': 'https://sandbox.api.bnpparibasfortis.com/psd2/v3',
        'redirect_uri': 'http://www.localhost:5000/dashboard/redirect',
        'brand': 'hb',
    },
}


def initialize_bank_api(bank):
    """Initialize BankAPI instance for the given bank."""
    bank_config = BANK_CONFIGURATIONS.get(bank)
    if not bank_config:
        return "Invalid bank selected", 400
    return BankAPI(bank_config), None


def authenticate_user(bank_api, username, password):
    """Authenticate the user and return an access token."""
    access_token = bank_api.get_access_token(username, password)
    if not access_token:
        return "Authentication failed", 400
    return access_token, None


def combine_data(bank_api, access_token):
    """Fetch transaction and balance data."""
    ibans = bank_api.get_ibans(access_token)
    if not ibans:
        return "Failed to retrieve IBANs", 400
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
    return data, 200