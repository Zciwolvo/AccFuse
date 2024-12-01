from .BankAPI import BankAPI 
from ..database import database as db
from ..database.Models.Bank import Bank
from ..database.Models.Account import Account
from ..database.Models.Transaction import Transaction
from ..database.Models.Balance import Balance
from sqlalchemy.exc import IntegrityError
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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
        return "Authentication failed", 401
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

def save_to_database(user_id, state, account_data, transactions, balances):
    """
    Saves account data, transactions, and balances to the database.

    Args:
        user_id (int): The user ID.
        state (str): Bank identifier or name.
        account_data (dict): Account data retrieved from the API.
        transactions (list): List of transaction data for each account.
        balances (list): List of balance data for each account.
    """
    try:
        # Find or create the bank
        bank = db.session.query(Bank).filter_by(name=state).first()
        if not bank:
            bank = Bank(name=state, bic=account_data['accounts'][0].get('bicFi', ''))
            db.session.add(bank)
            db.session.flush()  # Flush to get bank_id

        for account_info, account_transactions, account_balances in zip(
            account_data['accounts'], transactions, balances
        ):
            # Check if account with the same resource_id already exists
            account = db.session.query(Account).filter_by(
                resource_id=account_info['resourceId'], user_id=user_id
            ).first()

            if account:
                # If account exists, delete related balances and transactions
                db.session.query(Balance).filter_by(account_id=account.account_id).delete()
                db.session.query(Transaction).filter_by(account_id=account.account_id).delete()
                db.session.delete(account)
                db.session.flush()  # Ensure deletion is committed before re-adding

            # Create a new account
            account = Account(
                user_id=user_id,
                bank_id=bank.bank_id,
                resource_id=account_info['resourceId'],
                iban=account_info['accountId']['iban'],
                name=account_info.get('name'),
                usage=account_info.get('usage'),
                cash_account_type=account_info.get('cashAccountType'),
                product=account_info.get('product'),
                currency=account_info['currency'],
                psu_status=account_info.get('psuStatus'),
            )
            db.session.add(account)
            db.session.flush()  # Flush to get account_id

            # Save balances, or add dummy balances if none exist
            if account_balances and account_balances.get('balances'):
                for balance in account_balances['balances']:
                    db.session.add(
                        Balance(
                            account_id=account.account_id,
                            name=balance.get('name'),
                            balance_type=balance.get('balanceType'),
                            reference_date=balance.get('referenceDate'),
                            amount=balance['balanceAmount']['amount'],
                            currency=balance['balanceAmount']['currency'],
                        )
                    )
            else:
                # Add dummy balances
                dummy_balances = [
                    ("Closing balance", "CLBD"),
                    ("Operational balance", "OTHR"),
                    ("Available Balance", "ITAV"),
                ]
                for name, balance_type in dummy_balances:
                    db.session.add(
                        Balance(
                            account_id=account.account_id,
                            name=name,
                            balance_type=balance_type,
                            reference_date=None,
                            amount=0.0,
                            currency="EUR",
                        )
                    )

            # Save transactions
            if account_transactions and account_transactions.get('transactions'):
                for transaction in account_transactions['transactions']:
                    db.session.add(
                        Transaction(
                            account_id=account.account_id,
                            resource_id=transaction.get('resourceId'),
                            entry_reference=transaction.get('entryReference'),
                            amount=transaction['transactionAmount'].get('amount'),
                            currency=transaction['transactionAmount'].get('currency'),
                            credit_debit_indicator=transaction.get('creditDebitIndicator'),
                            status=transaction.get('status'),
                            booking_date=transaction.get('bookingDate'),
                            value_date=transaction.get('valueDate'),
                            transaction_date=transaction.get('transactionDate'),
                            transaction_category_purpose=transaction.get('transactionCategoryPurpose'),
                            end_to_end_reference=transaction.get('endToEndReference'),
                            narrative=transaction.get('narrative'),
                            unstructured_remittance_info=transaction.get('unstructuredRemittanceInformation'),
                        )
                    )

        # Commit the session
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        raise RuntimeError(f"Database integrity error: {e}")

    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"An error occurred while saving to the database: {e}")

def update_account_status_in_db(account_id, active):
    """
    Updates the 'active' status of an account in the database.

    Args:
        account_id (int): The ID of the account to update.
        active (bool): The new status for the account.

    Returns:
        dict: A result containing a 'success' key (True/False) and additional data or an error message.
    """
    try:
        account = db.session.query(Account).filter_by(account_id=account_id).first()
        if not account:
            return {"success": False, "error": "Account not found."}
        if account.active:
            account.active = 0
        else:
            account.active = 1
        db.session.commit()

        status_message = "enabled" if account.active else "disabled"
        return {"success": True, "message": f"Account {account_id} has been {status_message} successfully."}

    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}
    
def delete_account(account_id):
    """
    Deletes an account and all related data (balances and transactions) from the database.

    Args:
        account_id (int): The ID of the account to delete.
    """
    try:
        # Find the account by ID
        account = db.session.query(Account).filter_by(account_id=account_id).first()
        if not account:
            raise ValueError(f"Account with ID {account_id} does not exist.")

        # Delete related balances and transactions
        db.session.query(Balance).filter_by(account_id=account.account_id).delete()
        db.session.query(Transaction).filter_by(account_id=account.account_id).delete()

        # Delete the account itself
        db.session.delete(account)

        # Commit the changes
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"An error occurred while deleting the account: {e}")


def analyze_and_predict_account(account_id, past_days=365, future_days=30):
    """
    Analyze account transactions and predict future trends.

    Parameters:
        account_id (int): The ID of the account to analyze.
        past_days (int): Number of past days to consider for analysis.
        future_days (int): Number of future days to predict balances for.

    Returns:
        dict: Analysis results with recurring payments, trends, and predictions.
    """
    # Fetch account details
    account = Account.query.get(account_id)
    if not account:
        return {"error": "Account not found"}

    # Define the date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=past_days)

    # Query past transactions
    transactions = Transaction.query.filter(
        Transaction.account_id == account_id,
        Transaction.booking_date.between(start_date, end_date)
    ).all()

    # Query the current balance
    balance = Balance.query.filter(
        Balance.account_id == account_id
    ).order_by(Balance.reference_date.desc()).first()

    if not transactions and not balance:
        return {"error": "No data available for analysis"}

    # Convert transactions to DataFrame
    transaction_df = pd.DataFrame([{
        "date": t.booking_date,
        "amount": float(t.amount) if t.credit_debit_indicator == "credit" else -float(t.amount),
        "narrative": t.narrative
    } for t in transactions])

    if not transaction_df.empty:
        transaction_df["date"] = pd.to_datetime(transaction_df["date"], errors='coerce')
        transaction_df.dropna(subset=["date"], inplace=True)
        transaction_df.sort_values("date", inplace=True)
    else:
        return {}

    # Identify recurring payments
    recurring_payments = identify_recurring_payments(transaction_df)
    recurring_payments = [
        {
            "narrative": str(payment["narrative"]),
            "median_interval_days": int(payment["median_interval_days"]),
            "average_amount": float(payment["average_amount"]),
        }
        for payment in recurring_payments
    ]

    # Analyze transaction trends
    transaction_trends = analyze_transaction_trends(transaction_df)
    if transaction_trends:
        transaction_trends = {
            "overall_trend": str(transaction_trends["overall_trend"]),
            "average_daily_change": float(transaction_trends["average_daily_change"]),
            "std_dev_change": float(transaction_trends["std_dev_change"]),
        }

    # Predict future balances based on transactions
    future_dates, predicted_changes = predict_future_changes(transaction_df, future_days)
    future_dates = [d.strftime('%Y-%m-%d') for d in future_dates]  # Convert to strings for JSON serialization
    predicted_changes = [float(change) for change in predicted_changes]

    # Adjust predictions with the current balance
    current_balance = float(balance.amount) if balance else 0.0
    predicted_balances = [float(current_balance + change) for change in predicted_changes]

    return {
        "account_id": int(account_id),
        "recurring_payments": recurring_payments,
        "transaction_trends": transaction_trends,
        "future_predictions": {
            "dates": future_dates,
            "predicted_balances": predicted_balances,
        }
    }


def analyze_transaction_trends(transaction_df):
    """
    Analyze transaction trends over time.
    """
    if transaction_df.empty:
        return {"trend": "No data"}

    # Group by date and calculate daily transaction totals
    daily_totals = transaction_df.groupby("date")["amount"].sum()

    # Assess trends
    trend = {
        "average_daily_change": daily_totals.mean(),
        "std_dev_change": daily_totals.std(),
        "overall_trend": "increasing" if daily_totals.mean() > 0 else "decreasing"
    }

    return trend


def predict_future_changes(transaction_df, future_days):
    """
    Predict future changes in balance based on transaction history.
    """
    if transaction_df.empty:
        return [], []

    # Group by date and calculate daily transaction totals
    daily_totals = transaction_df.groupby("date")["amount"].sum()
    average_daily_change = daily_totals.mean()

    # Predict future changes
    future_dates = [datetime.now().date() + timedelta(days=i) for i in range(1, future_days + 1)]
    predicted_changes = [i * average_daily_change for i in range(1, future_days + 1)]

    return future_dates, predicted_changes


def identify_recurring_payments(transaction_df):
    """
    Identify recurring payments by analyzing transactions.
    """
    if transaction_df.empty:
        return []

    # Ensure 'date' is in datetime format
    transaction_df["date"] = pd.to_datetime(transaction_df["date"], errors='coerce')
    transaction_df.dropna(subset=["date"], inplace=True)

    # Group by narrative or a defined pattern and detect frequency
    recurring = []
    for narrative, group in transaction_df.groupby("narrative"):
        dates = group["date"].sort_values()
        intervals = dates.diff().dt.days
        if intervals.median() < 35:  # Recurrence within ~1 month
            recurring.append({
                "narrative": narrative,
                "median_interval_days": intervals.median(),
                "average_amount": group["amount"].mean()
            })
    return recurring