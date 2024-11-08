from .. import database as db

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