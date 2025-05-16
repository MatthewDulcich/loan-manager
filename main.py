import tkinter as tk
from database.db import Database
from gui.app import LoanManagerApp

def main():
    # Initialize the database
    db = Database()
    db.connect()
    db.init_schema()

    # Set up the main application window
    root = tk.Tk()
    root.title("Loan Manager")
    root.geometry("800x600")

    # Initialize and run the main application
    app = LoanManagerApp(master=root, db=db)
    app.mainloop()

    # Close the database connection upon exiting the app
    db.close()

if __name__ == "__main__":
    main()