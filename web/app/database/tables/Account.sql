CREATE TABLE Account (
    account_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES User(user_id),
    bank_id INT REFERENCES Bank(bank_id),
    resource_id VARCHAR(50) UNIQUE NOT NULL,
    iban VARCHAR(34) UNIQUE NOT NULL,
    name VARCHAR(100),
    usage VARCHAR(10),           
    cash_account_type VARCHAR(4),  
    product VARCHAR(50),
    currency VARCHAR(3) NOT NULL,
    psu_status VARCHAR(10),       
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);