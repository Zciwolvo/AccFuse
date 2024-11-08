from .. import database as db

class RelatedParty(db.Model):
    __tablename__ = 'related_parties'
    party_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), nullable=False)
    role = db.Column(db.String(10))
    name = db.Column(db.String(100))
    bic = db.Column(db.String(11))
    account_iban = db.Column(db.String(34))