from . import database as db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    verified = db.Column(db.Boolean, default=False)

    accounts = db.relationship('Account', backref='user', lazy=True)

class Bank(db.Model):
    __tablename__ = 'banks'
    bank_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bic = db.Column(db.String(11), unique=True, nullable=False)

    accounts = db.relationship('Account', backref='bank', lazy=True)

class Account(db.Model):
    __tablename__ = 'accounts'
    account_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.bank_id'), nullable=False)
    resource_id = db.Column(db.String(50), unique=True, nullable=False)
    iban = db.Column(db.String(34), unique=True, nullable=False)
    name = db.Column(db.String(100))
    usage = db.Column(db.String(10))
    cash_account_type = db.Column(db.String(4))
    product = db.Column(db.String(50))
    currency = db.Column(db.String(3), nullable=False)
    psu_status = db.Column(db.String(10))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())

    balances = db.relationship('Balance', backref='account', lazy=True)
    transactions = db.relationship('Transaction', backref='account', lazy=True)

class Balance(db.Model):
    __tablename__ = 'balances'
    balance_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=False)
    name = db.Column(db.String(50))
    balance_type = db.Column(db.String(4))
    reference_date = db.Column(db.Date)
    amount = db.Column(db.Numeric(15, 2))
    currency = db.Column(db.String(3), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=False)
    resource_id = db.Column(db.Integer, unique=True, nullable=False)
    entry_reference = db.Column(db.String(30))
    amount = db.Column(db.Numeric(15, 2))
    currency = db.Column(db.String(3), nullable=False)
    credit_debit_indicator = db.Column(db.String(4))
    status = db.Column(db.String(10))
    booking_date = db.Column(db.Date)
    value_date = db.Column(db.Date)
    transaction_date = db.Column(db.Date)
    transaction_category_purpose = db.Column(db.String(20))
    end_to_end_reference = db.Column(db.String(50))
    narrative = db.Column(db.Text)
    unstructured_remittance_info = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    bank_transaction_codes = db.relationship('BankTransactionCode', backref='transaction', lazy=True)
    related_parties = db.relationship('RelatedParty', backref='transaction', lazy=True)

class BankTransactionCode(db.Model):
    __tablename__ = 'bank_transaction_codes'
    code_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), nullable=False)
    domain = db.Column(db.String(10))
    family = db.Column(db.String(10))
    sub_family = db.Column(db.String(10))

class RelatedParty(db.Model):
    __tablename__ = 'related_parties'
    party_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), nullable=False)
    role = db.Column(db.String(10))
    name = db.Column(db.String(100))
    bic = db.Column(db.String(11))
    account_iban = db.Column(db.String(34))
