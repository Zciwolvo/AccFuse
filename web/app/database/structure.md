// User Table
Table users {
user_id integer [primary key]
username varchar(50) [not null, unique]
password varchar(255) [not null] // Assume hashed password
email varchar(100) [not null, unique]
created_at timestamp [default: `current_timestamp`]
updated_at timestamp [default: `current_timestamp`]
}

// Bank Table
Table banks {
bank_id integer [primary key]
name varchar(100) [not null]
bic varchar(11) [not null, unique] // Bank Identifier Code
}

// Account Table
Table accounts {
account_id integer [primary key]
user_id integer [not null]
bank_id integer [not null]
resource_id varchar(50) [not null, unique]
iban varchar(34) [not null, unique]
name varchar(100)
usage varchar(10) // e.g., PRIV, BUSN
cash_account_type varchar(4) // e.g., CACC
product varchar(50)
currency varchar(3) [not null]
psu_status varchar(10) // e.g., Holder
created_at timestamp [default: `current_timestamp`]
updated_at timestamp [default: `current_timestamp`]
}

// Balance Table
Table balances {
balance_id integer [primary key]
account_id integer [not null]
name varchar(50) // e.g., Closing balance, Available balance
balance_type varchar(4) // e.g., CLBD, ITAV
reference_date date
amount decimal(15, 2)
currency varchar(3) [not null]
created_at timestamp [default: `current_timestamp`]
}

// Transaction Table
Table transactions {
transaction_id integer [primary key]
account_id integer [not null]
resource_id integer [not null, unique]
entry_reference varchar(30)
amount decimal(15, 2)
currency varchar(3) [not null]
credit_debit_indicator varchar(4) // e.g., CRDT, DBIT
status varchar(10) // e.g., BOOK
booking_date date
value_date date
transaction_date date
transaction_category_purpose varchar(20) // e.g., SALA
end_to_end_reference varchar(50)
narrative text
unstructured_remittance_info text
created_at timestamp [default: `current_timestamp`]
}

// BankTransactionCode Table
Table bank_transaction_codes {
code_id integer [primary key]
transaction_id integer [not null]
domain varchar(10)
family varchar(10)
sub_family varchar(10)
}

// RelatedParty Table
Table related_parties {
party_id integer [primary key]
transaction_id integer [not null]
role varchar(10) // e.g., debtor, creditor
name varchar(100)
bic varchar(11)
account_iban varchar(34)
}

// Relationships
Ref: accounts.user_id > users.user_id
Ref: accounts.bank_id > banks.bank_id
Ref: balances.account_id > accounts.account_id
Ref: transactions.account_id > accounts.account_id
Ref: bank_transaction_codes.transaction_id > transactions.transaction_id
Ref: related_parties.transaction_id > transactions.transaction_id
