from flask import render_template, session, current_app as app, redirect, request, jsonify, url_for
from . import dashboard
from ..database.Models.Account import Account
from ..database.Models.Transaction import Transaction
from ..database.Models.Balance import Balance
from flask_jwt_extended import get_jwt_identity, jwt_required
from .BankController import BANK_CONFIGURATIONS, initialize_bank_api, authenticate_user, combine_data, save_to_database, delete_account, update_account_status_in_db, analyze_and_predict_account
from datetime import datetime
from sqlalchemy.sql import func
from collections import defaultdict


@dashboard.route('/dashboard', methods=['GET', 'POST'])
@jwt_required()
def index():
    user_id = get_jwt_identity()
    user_accounts = get_user_accounts(user_id)

    # Filter out inactive accounts
    active_accounts = [account for account in user_accounts if account.active]

    # Get year filter
    selected_year = request.args.get('selected_year', type=int, default=datetime.now().year)
    available_years = get_available_years(active_accounts)

    # Parse transaction filters from the request
    filters = parse_filters(request)

    # Convert date strings to actual date objects
    if filters['start_date']:
        filters['start_date'] = datetime.strptime(filters['start_date'], '%Y-%m-%d')
    if filters['end_date']:
        filters['end_date'] = datetime.strptime(filters['end_date'], '%Y-%m-%d')

    # Get filtered transactions
    all_transactions = get_filtered_transactions(active_accounts, filters)
    transactions = get_yearly_transactions(active_accounts, selected_year)

    # Prepare month-by-month analytics (combined and account-specific)
    (
        monthly_data,
        monthly_labels,
        monthly_net_changes,
        monthly_utilizations,
        account_monthly_data,
    ) = calculate_monthly_analytics(transactions, active_accounts)

    # Prepare bar chart data (combined and account-specific)
    incomes, outcomes, bar_labels, account_bar_data = calculate_bar_chart_data(active_accounts, transactions)

    # Prepare pie chart data (combined and account-specific)
    pie_labels, pie_data = calculate_pie_chart_data(active_accounts)

    # Handle the prediction form inputs
    past_days = request.args.get('past_days', default=365, type=int)
    future_days = request.args.get('future_days', default=30, type=int)

    prediction_results = {}
    past_days = request.args.get('past_days', 365, type=int)
    future_days = request.args.get('future_days', 30, type=int)

    # Initialize combined summary
    combined_data = {
        "future_predictions": {
            "dates": [],
            "predicted_balances": []
        }
    }

    # Collect data for combination
    combined_dates = set()
    combined_balances = defaultdict(float)

    for account in active_accounts:
        prediction = analyze_and_predict_account(account.account_id, past_days, future_days)
        if prediction:
            # Find the corresponding user account by account_id
            matching_account = next(
                (user_account for user_account in user_accounts if user_account.account_id == prediction["account_id"]),
                None
            )
            if matching_account:
                prediction["name"] = matching_account.name
            else:
                prediction["name"] = f"Account {prediction['account_id']}"
            
            prediction_results[account.account_id] = prediction 
            
            # Collect combined data
            dates = prediction["future_predictions"]["dates"]
            balances = prediction["future_predictions"]["predicted_balances"]
            for date, balance in zip(dates, balances):
                combined_dates.add(date)
                combined_balances[date] += balance

    # Prepare combined summary for chart
    if combined_balances:
        sorted_combined_dates = sorted(combined_dates)  # Sort dates
        combined_data["future_predictions"]["dates"] = sorted_combined_dates
        combined_data["future_predictions"]["predicted_balances"] = [
            combined_balances[date] for date in sorted_combined_dates
        ]
        prediction_results["combined"] = combined_data
    return render_template(
        'dashboard.html',
        has_accounts=bool(user_accounts),
        accounts=user_accounts,
        transactions=transactions,
        all_transactions=all_transactions,
        bar_labels=bar_labels,
        incomes=incomes,
        outcomes=outcomes,
        pie_labels=pie_labels,
        pie_data=pie_data,
        monthly_data=monthly_data,
        monthly_labels=monthly_labels,
        monthly_net_changes=monthly_net_changes,
        monthly_utilizations=monthly_utilizations,
        available_years=available_years,
        selected_year=selected_year,
        account_monthly_data=account_monthly_data, 
        account_bar_data=account_bar_data,
        prediction_results=prediction_results
    )


    
def get_user_accounts(user_id):
    """Retrieve accounts for a given user."""
    return Account.query.filter_by(user_id=user_id).all()

def parse_filters(request):
    """Extract filters from request parameters."""
    return {
        'min_amount': request.args.get('min_amount', type=float, default=None),
        'max_amount': request.args.get('max_amount', type=float, default=None),
        'start_date': request.args.get('start_date', type=str, default=None),
        'end_date': request.args.get('end_date', type=str, default=None),
        'transaction_type': request.args.get('transaction_type', default=None),  # 'CRDT' or 'DBIT'
        'iban': request.args.get('iban', type=str, default=None),
        'description': request.args.get('description', type=str, default=None),
        'account_name': request.args.get('account_name', type=str, default=None),
    }

def get_filtered_transactions(user_accounts, filters):
    """Filter transactions based on user accounts and applied filters."""
    transactions_query = Transaction.query.filter(
        Transaction.account_id.in_([a.account_id for a in user_accounts])
    )
    
    if filters['min_amount']:
        transactions_query = transactions_query.filter(Transaction.amount >= filters['min_amount'])
    if filters['max_amount']:
        transactions_query = transactions_query.filter(Transaction.amount <= filters['max_amount'])
    if filters['start_date']:
        transactions_query = transactions_query.filter(Transaction.booking_date >= filters['start_date'])
    if filters['end_date']:
        transactions_query = transactions_query.filter(Transaction.booking_date <= filters['end_date'])
    if filters['transaction_type']:
        transactions_query = transactions_query.filter(Transaction.credit_debit_indicator == filters['transaction_type'])
    if filters['iban']:
        transactions_query = transactions_query.filter(Transaction.iban.ilike(f"%{filters['iban']}%"))
    if filters['description']:
        transactions_query = transactions_query.filter(Transaction.description.ilike(f"%{filters['description']}%"))
    if filters['account_name']:
        transactions_query = transactions_query.filter(Transaction.account_name.ilike(f"%{filters['account_name']}%"))
    
    return transactions_query.all()



def calculate_bar_chart_data(user_accounts, transactions):
    """Calculate data for the bar chart showing incomes and outcomes."""
    global_incomes = 0
    global_outcomes = 0
    account_bar_data = []

    for account in user_accounts:
        account_transactions = [t for t in transactions if t.account_id == account.account_id]
        total_income = sum(float(t.amount) for t in account_transactions if t.credit_debit_indicator == 'CRDT')
        total_outcome = sum(abs(float(t.amount)) for t in account_transactions if t.credit_debit_indicator == 'DBIT')

        global_incomes += total_income
        global_outcomes += total_outcome

        account_bar_data.append({
            "account_name": account.name,
            "income": total_income,
            "outcome": total_outcome,
        })

    # Global bar chart data
    bar_labels = ["Combined Data"]
    incomes = [global_incomes]
    outcomes = [global_outcomes]

    # Add individual account data
    bar_labels.extend(account["account_name"] for account in account_bar_data)
    incomes.extend(account["income"] for account in account_bar_data)
    outcomes.extend(account["outcome"] for account in account_bar_data)

    return incomes, outcomes, bar_labels, account_bar_data

def calculate_pie_chart_data(user_accounts):
    """Calculate data for the pie chart showing fund distribution."""
    balances = Balance.query.filter(
        Balance.account_id.in_([a.account_id for a in user_accounts])
    ).all()
    
    pie_labels = [a.name for a in user_accounts]
    pie_data = [sum(float(b.amount) for b in balances if b.account_id == account.account_id and b.balance_type == "OTHR") for account in user_accounts]
    
    return pie_labels, pie_data

def get_available_years(user_accounts):
    transaction_years = Transaction.query.with_entities(
        func.year(Transaction.booking_date).label('year')
    ).filter(
        Transaction.account_id.in_([a.account_id for a in user_accounts])
    ).distinct().all()
    return sorted([year.year for year in transaction_years])

def get_yearly_transactions(user_accounts, year):
    return Transaction.query.filter(
        Transaction.account_id.in_([a.account_id for a in user_accounts]),
        func.year(Transaction.booking_date) == year
    ).all()
    
    
def calculate_monthly_analytics(transactions, current_users):
    monthly_labels = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Initialize global data structures
    monthly_net_changes = [0] * 12
    monthly_utilizations = [0] * 12
    account_monthly_data = {}  # Store per-account data

    # Prepare account-specific data structure
    for account in current_users:
        account_monthly_data[account.name] = {
            "monthly_net_changes": [0] * 12,
            "monthly_utilizations": [0] * 12,
        }

    # Process transactions
    for transaction in transactions:
        month = transaction.booking_date.month - 1  # Convert to 0-indexed
        amount = float(transaction.amount)
        account_id = transaction.account_id

        # Find the account name from current_users
        account_name = next(
            (account.name for account in current_users if account.account_id == account_id),
            None
        )
        if not account_name:
            continue  # Skip transactions for accounts not in current_users

        # Update global net changes and utilizations
        if transaction.credit_debit_indicator == "CRDT":
            monthly_net_changes[month] += amount
        elif transaction.credit_debit_indicator == "DBIT":
            monthly_net_changes[month] -= abs(amount)

        monthly_utilizations[month] += 1

        # Update account-specific data
        if transaction.credit_debit_indicator == "CRDT":
            account_monthly_data[account_name]["monthly_net_changes"][month] += amount
        elif transaction.credit_debit_indicator == "DBIT":
            account_monthly_data[account_name]["monthly_net_changes"][month] -= abs(amount)

        account_monthly_data[account_name]["monthly_utilizations"][month] += 1

    # Prepare combined monthly data for table
    monthly_data = []
    for i in range(12):
        monthly_data.append({
            "month": monthly_labels[i],
            "incomes": sum(
                float(t.amount) for t in transactions
                if t.booking_date.month == i + 1 and t.credit_debit_indicator == "CRDT"
            ),
            "outcomes": sum(
                abs(float(t.amount)) for t in transactions
                if t.booking_date.month == i + 1 and t.credit_debit_indicator == "DBIT"
            ),
            "net_change": monthly_net_changes[i],
        })

    return monthly_data, monthly_labels, monthly_net_changes, monthly_utilizations, account_monthly_data


@dashboard.route('/update_account_status', methods=['POST'])
@jwt_required()
def update_account_status():
    """
    Flask route to handle account status updates.
    Expects a POST request with JSON payload:
    {
        "account_id": <account_id>,
        "active": <true/false>
    }
    """
    data = request.get_json()
    account_id = data.get('account_id')
    active = data.get('active')

    if account_id is None or active is None:
        return jsonify({"error": "Account ID and status are required."}), 400

    # Call the database function
    result = update_account_status_in_db(account_id, active)

    # Handle response based on the result
    if result["success"]:
        return jsonify({"message": result["message"]}), 200
    else:
        return jsonify({"error": result.get("error", "An error occurred.")}), 500


@dashboard.route('/delete_account', methods=['POST'])
def delete_account_route():
    """
    Flask route to handle the deletion of an account and its related data.

    Expects a POST request with JSON payload:
    {
        "account_id": <account_id>
    }
    """
    try:
        # Parse the account_id from the request
        data = request.get_json()
        account_id = data.get('account_id')

        if not account_id:
            return jsonify({"error": "Account ID is required."}), 400

        # Call the delete_account function
        delete_account(account_id)

        return jsonify({"message": f"Account {account_id} and related data deleted successfully."}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dashboard.route('/connect_bank')
@jwt_required()
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
@jwt_required()
def bank_login(bank):
    """Renders login page or processes user login."""
    bank_config = BANK_CONFIGURATIONS.get(bank)
    if not bank_config:
        return render_template('bank_login.html', bank_name=bank.capitalize(), bank=bank, error="Invalid bank selected"), 400

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Initialize BankAPI
        bank_api, error = initialize_bank_api(bank)
        if error:
            return render_template('bank_login.html', bank_name=bank.capitalize(), bank=bank, error=f"Error initializing bank API: {error}"), 500

        # Authenticate user
        access_token, error = authenticate_user(bank_api, username, password)
        if error:
            return render_template('bank_login.html', bank_name=bank.capitalize(), bank=bank, error=f"Authentication failed: {error}"), 401

        # Generate authorization URL
        try:
            ibans = bank_api.get_ibans(access_token)
            authorization_code = bank_api.get_authorization_code(access_token, ibans)
            authorization_url = (
                f"{bank_config['auth_base_url']}/cardsAuthorizeConfirm"
                f"?code={authorization_code}&redirectTo={bank_config['redirect_uri']}"
                f"&state={bank}&appName=AccFuse&cards=N"
            )
        except Exception as e:
            return render_template('bank_login.html', bank_name=bank.capitalize(), bank=bank, error=f"Failed to generate authorization URL: {str(e)}"), 500

        # Redirect user to bank's authorization page
        return redirect(authorization_url)

    return render_template('bank_login.html', bank_name=bank.capitalize(), bank=bank, error="")




@dashboard.route('/dashboard/redirect', methods=['GET'])
@jwt_required()
def handle_redirect():
    """Handle redirect from the bank after authorization."""
    authorization_code = request.args.get('code')
    state = request.args.get('state')
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
    
    user_id = get_jwt_identity()
    save_to_database(user_id, state, account_data, transactions, balances)

    return redirect(url_for('dashboard.index')) 