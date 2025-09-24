# Loan Manager Application

The **Loan Manager Application** is a Python-based tool designed to help users manage their loans, calculate payoff plans, and visualize repayment strategies using various methods such as Snowball, Avalanche, and Custom strategies. The application features a graphical user interface (GUI) built with `tkinter` and integrates with an SQLite database for loan storage and management.

---

## Features

- **Loan Management**: Add, view, and delete loans with details such as principal, interest rate, and minimum monthly payment.
- **CSV Import**: Import multiple loans from a CSV file for bulk data entry.
- **Repayment Strategies**:
  - **Snowball Strategy**: Prioritizes loans with the smallest balances.
  - **Avalanche Strategy**: Prioritizes loans with the highest interest rates.
  - **Custom Strategy**: Allows users to define their own loan repayment order.
- **Payoff Plan Visualization**: Generate and display detailed payoff plans, including payment schedules, balances, and extra payments.
- **Interactive Editing**: Modify extra payments directly in the payoff plan table.
- **Export Functionality**: Save payoff plans to a text file for offline use.
- **Database Integration**: Store loan data persistently using SQLite.
- **Amortization Schedule**: Generate detailed amortization schedules for individual loans.

---

## Requirements

The application requires Python 3.8 or higher. The following Python libraries are used:

- `tkinter`
- `matplotlib`
- `SQLAlchemy`
- `pandas`
- `tkcalendar`

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/loan-manager.git
cd loan-manager
```

> **Note:** Use the command from the main directory to run files in folders, e.g.:
>
> ```bash
> python -m tests.test_models
> ```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

The application uses an SQLite database. The database schema is defined in `database/schema.sql`. The database will be automatically initialized when you run the application for the first time.

---

## Running the Application

To start the Loan Manager application, run the following command from the main directory:

```bash
python main.py
```

This will launch the GUI, where you can manage loans, generate payoff plans, and explore repayment strategies.

---

## Usage

### Adding a Loan
1. Click the **"Add Loan"** button in the main interface.
2. Fill in the loan details, including:
   - Loan Name
   - Principal Amount
   - Current Balance
   - Interest Rate
   - Monthly Minimum Payment
   - Extra Payment (optional)
   - First Due Date
3. Click **"Submit"** to save the loan.

### Importing Loans from CSV
1. Click the **"Import CSV"** button in the main interface.
2. Select your CSV file using the file dialog.
3. The application will validate and import your loans, showing a summary of results.

#### CSV Format Requirements
Your CSV file must contain the following columns (column names must match exactly):

**Required Columns:**
- `name`: Loan name/description
- `principal`: Original loan amount (numeric)
- `current_balance`: Current outstanding balance (numeric)
- `interest_rate`: Annual interest rate as percentage (e.g., 4.25)
- `monthly_min_payment`: Minimum monthly payment amount (numeric)
- `first_due_date`: First payment due date in YYYY-MM-DD format

**Optional Columns:**
- `extra_payment`: Additional payment amount (default: 0)
- `lender`: Name of the lending institution
- `loan_term_months`: Total loan term in months (numeric)
- `notes`: Additional notes about the loan

#### CSV Example
```csv
name,principal,current_balance,interest_rate,monthly_min_payment,extra_payment,first_due_date,lender,loan_term_months,notes
Student Loan,25000.00,22500.50,4.25,350.00,0.00,2025-01-15,Federal Direct,120,Federal student loan
Car Loan,18000.00,15200.75,6.50,425.00,50.00,2025-02-01,Chase Bank,60,2022 Honda Civic
Credit Card,5500.00,3200.25,18.99,125.00,0.00,2025-01-10,Capital One,,High interest debt
```

A template CSV file (`loan_template.csv`) is included in the project directory for reference.

### Viewing Loans
- All loans are displayed in a table on the main interface.
- Loans are sorted based on the selected repayment strategy.

### Generating a Payoff Plan
1. Select a repayment strategy from the dropdown menu:
   - Snowball
   - Avalanche
   - Custom
2. Click **"Export Payoff Plan"** to generate and view the payoff plan.
3. Modify extra payments directly in the payoff plan table if needed.

### Exporting a Payoff Plan
- Click **"Save to File"** in the payoff plan popup to save the plan as a text file (`payoff_plan.txt`).

---

## Running Tests

To run the tests, use the following command from the main directory:

```bash
python -m tests.test_models
```

You can replace `tests.test_models` with other test modules as needed, such as `tests.test_database` or `tests.test_strategies`.

---

## Configuration

The application configuration is defined in `config.py`. Key settings include:

- **Database Path:** `DB_PATH`
- **Schema Path:** `SCHEMA_PATH`
- **GUI Settings:** `WINDOW_TITLE`, `WINDOW_SIZE`
- **Logging:** `LOG_FILE`, `LOG_LEVEL`