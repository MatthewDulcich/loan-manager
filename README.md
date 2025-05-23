# Loan Manager Application

The **Loan Manager Application** is a Python-based tool designed to help users manage their loans, calculate payoff plans, and visualize repayment strategies using various methods such as Snowball, Avalanche, and Custom strategies. The application features a graphical user interface (GUI) built with `tkinter` and integrates with an SQLite database for loan storage and management.

---

## Features

- **Loan Management**: Add, view, and delete loans with details such as principal, interest rate, and minimum monthly payment.
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