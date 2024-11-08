CREATE TABLE Balance (
    balance_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES Account(account_id),
    name VARCHAR(50),           
    balance_type VARCHAR(4),     
    reference_date DATE,
    amount DECIMAL(15, 2),
    currency VARCHAR(3) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
