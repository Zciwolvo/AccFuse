CREATE TABLE RelatedParty (
    party_id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES Transaction(transaction_id),
    role VARCHAR(10),           
    name VARCHAR(100),
    bic VARCHAR(11),
    account_iban VARCHAR(34)
);