import sqlite3
import os
from typing import List
from models import Loan

# Define the path to your database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'loans.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Establish a connection to the SQLite database."""
        try:
            print(f"Attempting to connect to database at {self.db_path}")  # Add this line
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable name-based access to columns
            print(f"Connected to database at {self.db_path}")
        except sqlite3.Error as e:
            print(f"Connection failed: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def init_schema(self, schema_path=SCHEMA_PATH):
        """Initialize the database schema from a SQL file."""
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema file not found at {schema_path}")
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        try:
            self.conn.executescript(schema_sql)
            self.conn.commit()
            print("Database schema initialized.")
        except sqlite3.Error as e:
            print(f"Schema initialization failed: {e}")
            raise

    def execute(self, query, params=None):
        """Execute a single query with optional parameters."""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Query execution failed: {e}")
            raise

    def fetchall(self, query, params=None):
        """Fetch all rows from a query."""
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def fetchone(self, query, params=None):
        """Fetch a single row from a query."""
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def add_loan_priority(self, strategy_id: int, loan_id: int, priority: int):
        """
        Add or update the priority of a loan within a specific strategy.
        """
        query = """
            INSERT INTO loan_priority (strategy_id, loan_id, priority)
            VALUES (?, ?, ?)
            ON CONFLICT(strategy_id, loan_id) DO UPDATE SET priority=excluded.priority;
        """
        self.execute(query, (strategy_id, loan_id, priority))

    def get_loans_by_strategy(self, strategy_id: int) -> List[Loan]:
        """
        Retrieve loans associated with a specific strategy, ordered by priority.
        """
        query = """
            SELECT l.*
            FROM loans l
            JOIN loan_priority lp ON l.id = lp.loan_id
            WHERE lp.strategy_id = ?
            ORDER BY lp.priority ASC;
        """
        rows = self.fetchall(query, (strategy_id,))
        return [Loan.from_row(row) for row in rows]

    def delete_loan(self, loan_id):
        """Delete a loan by its ID."""
        with self.conn:
            self.conn.execute("DELETE FROM loans WHERE id = ?", (loan_id,))
    
if __name__ == "__main__":
    db = Database()
    db.connect()
    db.init_schema()

    # Example: Insert a new loan
    insert_query = """
    INSERT INTO loans (name, principal, current_balance, interest_rate, monthly_min_payment, first_due_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    loan_data = ("Student Loan A", 10000.0, 10000.0, 5.0, 150.0, "2025-06-01")
    db.execute(insert_query, loan_data)

    # Example: Add loan priority
    db.add_loan_priority(strategy_id=1, loan_id=1, priority=1)

    # Example: Retrieve loans by strategy
    loans = db.get_loans_by_strategy(strategy_id=1)
    for loan in loans:
        print(vars(loan))

    db.close()