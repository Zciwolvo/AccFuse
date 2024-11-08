CREATE TABLE Transaction (
    transaction_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES Account(account_id),
    resource_id INT UNIQUE NOT NULL,
    entry_reference VARCHAR(30),
    amount DECIMAL(15, 2),
    currency VARCHAR(3) NOT NULL,
    credit_debit_indicator CHAR(4),  
    status VARCHAR(10),         
    booking_date DATE,
    value_date DATE,
    transaction_date DATE,
    transaction_category_purpose VARCHAR(20),
    end_to_end_reference VARCHAR(50),
    narrative TEXT,
    unstructured_remittance_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
