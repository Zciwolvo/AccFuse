import pandas as pd
import random
from datetime import datetime, timedelta

# Function to generate realistic transaction data
def generate_transactions(account_id, start_date, end_date, num_transactions=500):
    transaction_data = []
    current_date = start_date

    for _ in range(num_transactions):
        transaction = {
            "transaction_id": random.randint(10000, 99999),
            "account_id": account_id,
            "resource_id": random.randint(100000, 999999),
            "entry_reference": f"REF-{random.randint(1000, 9999)}",
            "amount": round(random.uniform(-500, 500), 2),  # Random amounts
            "currency": "EUR",
            "status": random.choice(["BOOKED", "PENDING"]),
            "booking_date": current_date.strftime("%Y-%m-%d"),
            "value_date": (current_date + timedelta(days=random.randint(0, 2))).strftime("%Y-%m-%d"),
            "transaction_date": current_date.strftime("%Y-%m-%d"),
            "transaction_category_purpose": random.choice(["SALARY", "RENT", "GROCERIES", "UTILITIES", "ENTERTAINMENT"]),
            "end_to_end_reference": f"END-{random.randint(1000, 9999)}",
            "narrative": random.choice([
                "Salary Payment", "Grocery Shopping", "Monthly Rent", 
                "Utility Bill", "Entertainment Expenses", "Miscellaneous"
            ]),
            "unstructured_remittance_info": random.choice([
                "Invoice 12345", "Payment for services", "Subscription fee",
                "Overdraft repayment", "Refund", "Loan EMI"
            ]),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if transaction["amount"] > 0:
            transaction["credit_debit_indicator"] = "CRDT"
        else:
            transaction["credit_debit_indicator"] = "DBIT"
        transaction_data.append(transaction)
        current_date += timedelta(days=random.randint(1, 5))  # Add random days for next transaction

        if current_date > end_date:
            break

    return transaction_data

# Define date range for transactions
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 10, 31)

# Generate transactions for account_id 3 and 4
transactions_account_3 = generate_transactions(account_id=3, start_date=start_date, end_date=end_date)
transactions_account_4 = generate_transactions(account_id=4, start_date=start_date, end_date=end_date)

# Combine transactions
all_transactions = transactions_account_3 + transactions_account_4

# Convert to DataFrame
df_transactions = pd.DataFrame(all_transactions)

# Save to CSV
csv_path = "transactions.csv"
df_transactions.to_csv(csv_path, index=False)