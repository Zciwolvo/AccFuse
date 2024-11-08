CREATE TABLE BankTransactionCode (
    code_id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES Transaction(transaction_id),
    domain VARCHAR(10),
    family VARCHAR(10),
    sub_family VARCHAR(10)
);