-- Table: loans
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    principal REAL NOT NULL CHECK (principal >= 0),  -- Original loan amount
    current_balance REAL NOT NULL CHECK (current_balance >= 0),  -- Outstanding balance
    interest_rate REAL NOT NULL CHECK (interest_rate >= 0),  -- Annual interest rate (%)
    monthly_min_payment REAL NOT NULL CHECK (monthly_min_payment >= 0),
    extra_payment REAL DEFAULT 0 CHECK (extra_payment >= 0),  -- Extra monthly payment
    first_due_date TEXT NOT NULL,  -- ISO format date (YYYY-MM-DD)
    interest_change_rate REAL DEFAULT 0,  -- Annual interest rate change (%)
    loan_term_months INTEGER,  -- Total loan term in months
    lender TEXT,
    notes TEXT,
    forbearance_start_date TEXT,  -- ISO format date
    forbearance_end_date TEXT,    -- ISO format date
    total_paid REAL DEFAULT 0 CHECK (total_paid >= 0),  -- Total amount paid
    last_payment_date TEXT,  -- ISO format date
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Table: payoff_strategies
CREATE TABLE IF NOT EXISTS payoff_strategies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_name TEXT NOT NULL,  -- e.g., 'snowball', 'avalanche', 'custom'
    extra_payment REAL DEFAULT 0 CHECK (extra_payment >= 0),  -- Global extra payment
    total_monthly_budget REAL DEFAULT 0 CHECK (total_monthly_budget >= 0),
    custom_order TEXT,  -- JSON array of loan IDs for custom strategy
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Table: payments
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    payment_date TEXT NOT NULL,  -- ISO format date
    strategy_id INTEGER,  -- Nullable: linked strategy
    FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE,
    FOREIGN KEY (strategy_id) REFERENCES payoff_strategies(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS loan_priority (
    strategy_id INTEGER NOT NULL,
    loan_id INTEGER NOT NULL,
    priority INTEGER NOT NULL,
    PRIMARY KEY (strategy_id, loan_id),
    FOREIGN KEY (strategy_id) REFERENCES payoff_strategies(id) ON DELETE CASCADE,
    FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
);