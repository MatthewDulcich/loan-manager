import tkinter as tk
from database.db import Database
from gui.app import LoanManagerApp

def main():
    # Initialize the database
    db = Database()
    db.connect()
    db.init_schema()

    # Initialize and run the main application
    app = LoanManagerApp(db=db)
    app.title("Loan Manager")
    app.geometry("800x600")
    app.mainloop()

    # Close the database connection upon exiting the app
    db.close()

if __name__ == "__main__":
    main()