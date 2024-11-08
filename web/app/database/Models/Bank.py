from .. import database as db

class Bank(db.Model):
    __tablename__ = 'banks'
    bank_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bic = db.Column(db.String(11), unique=True, nullable=False)

    accounts = db.relationship('Account', backref='bank', lazy=True)