from .. import database as db

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