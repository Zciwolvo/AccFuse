from .. import database as db

class BankTransactionCode(db.Model):
    __tablename__ = 'bank_transaction_codes'
    code_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), nullable=False)
    domain = db.Column(db.String(10))
    family = db.Column(db.String(10))
    sub_family = db.Column(db.String(10))