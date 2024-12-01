from .. import database as db

class Account(db.Model):
    __tablename__ = 'accounts'
    account_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.bank_id'), nullable=False)
    resource_id = db.Column(db.String(50), nullable=False)
    iban = db.Column(db.String(34), nullable=False)
    name = db.Column(db.String(100))
    usage = db.Column(db.String(10))
    cash_account_type = db.Column(db.String(4))
    product = db.Column(db.String(50))
    currency = db.Column(db.String(3), nullable=False)
    psu_status = db.Column(db.String(10))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())

    balances = db.relationship('Balance', backref='account', lazy=True)
    transactions = db.relationship('Transaction', backref='account', lazy=True)