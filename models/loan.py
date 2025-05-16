from datetime import datetime, timedelta, date

class Loan:
    def __init__(self, id, name, principal, current_balance, interest_rate,
                 monthly_min_payment, extra_payment, first_due_date,
                 interest_change_rate=0.0, loan_term_months=None, lender=None,
                 notes=None, forbearance_start_date=None, forbearance_end_date=None,
                 total_paid=0.0, last_payment_date=None, created_at=None):
        self.id = id
        self.name = name
        self.principal = principal
        self.current_balance = current_balance
        self.interest_rate = interest_rate  # Annual percentage rate
        self.monthly_min_payment = monthly_min_payment
        self.extra_payment = extra_payment
        self.first_due_date = self._parse_date(first_due_date)
        self.interest_change_rate = interest_change_rate
        self.loan_term_months = loan_term_months
        self.lender = lender
        self.notes = notes
        self.forbearance_start_date = self._parse_date(forbearance_start_date)
        self.forbearance_end_date = self._parse_date(forbearance_end_date)
        self.total_paid = total_paid
        self.last_payment_date = self._parse_date(last_payment_date)
        self.created_at = self._parse_date(created_at) if created_at else datetime.today().date()

    @staticmethod
    def _parse_date(value):
        if value is None:
            return None
        if isinstance(value, date):
            return value
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(value, fmt).date()
            except (ValueError, TypeError):
                continue
        raise ValueError(f"Date '{value}' is not in a recognized format")

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            name=row["name"],
            principal=row["principal"],
            current_balance=row["current_balance"],
            interest_rate=row["interest_rate"],
            monthly_min_payment=row["monthly_min_payment"],
            extra_payment=row["extra_payment"],
            first_due_date=row["first_due_date"],
            interest_change_rate=row["interest_change_rate"],
            loan_term_months=row["loan_term_months"],
            lender=row["lender"],
            notes=row["notes"],
            forbearance_start_date=row["forbearance_start_date"],
            forbearance_end_date=row["forbearance_end_date"],
            total_paid=row["total_paid"],
            last_payment_date=row["last_payment_date"],
            created_at=row["created_at"]
        )

    def is_in_forbearance(self, check_date=None):
        """Check if the loan is in forbearance on the given date."""
        if not self.forbearance_start_date or not self.forbearance_end_date:
            return False
        check_date = check_date or datetime.today().date()
        return self.forbearance_start_date <= check_date <= self.forbearance_end_date

    def calculate_accrued_interest(self, from_date=None, to_date=None):
        """Calculate accrued interest between two dates."""
        from_date = from_date or self.last_payment_date or self.first_due_date
        to_date = to_date or datetime.today().date()
        if from_date >= to_date:
            return 0.0

        # Skip interest accrual during forbearance
        if self.is_in_forbearance(to_date):
            return 0.0

        days = (to_date - from_date).days
        daily_rate = self.interest_rate / 100 / 365
        accrued_interest = self.current_balance * daily_rate * days
        return round(accrued_interest, 2)

    def apply_payment(self, amount, payment_date=None):
        """Apply a payment to the loan."""
        if payment_date is None:
            payment_date = datetime.today().date()
        elif isinstance(payment_date, str):
            payment_date = datetime.strptime(payment_date, "%Y-%m-%d").date()
        accrued_interest = self.calculate_accrued_interest(self.last_payment_date, payment_date)
        self.current_balance += accrued_interest

        interest_payment = min(amount, accrued_interest)
        principal_payment = max(0.0, amount - interest_payment)
        self.current_balance = max(0.0, self.current_balance - principal_payment)
        self.total_paid += amount
        self.last_payment_date = payment_date

        return {
            "interest_paid": round(interest_payment, 2),
            "principal_paid": round(principal_payment, 2),
            "remaining_balance": round(self.current_balance, 2)
        }

    def generate_amortization_schedule(self):
        """Generate an amortization schedule."""
        schedule = []
        balance = self.current_balance
        monthly_rate = self.interest_rate / 100 / 12
        payment = self.monthly_min_payment + self.extra_payment
        payment_date = self.first_due_date

        while balance > 0:
            interest = balance * monthly_rate
            principal = payment - interest
            if principal > balance:
                principal = balance
                payment = principal + interest
            balance -= principal
            schedule.append({
                "date": payment_date,
                "payment": round(payment, 2),
                "principal": round(principal, 2),
                "interest": round(interest, 2),
                "balance": round(balance, 2)
            })
            payment_date += timedelta(days=30)  # Approximate next month

        return schedule

if __name__ == "__main__":
    # Example loan for testing
    loan = Loan(
        id=1,
        name="Test Loan",
        principal=10000.0,
        current_balance=10000.0,
        interest_rate=5.0,
        monthly_min_payment=200.0,
        extra_payment=50.0,
        first_due_date="2025-06-01"
    )

    print("Initial loan state:")
    print(vars(loan))

    # Apply a payment
    payment_result = loan.apply_payment(300.0, payment_date="2025-07-01")
    print("\nAfter payment:")
    print(payment_result)
    print(vars(loan))

    # Generate amortization schedule
    print("\nAmortization schedule (first 5 months):")
    schedule = loan.generate_amortization_schedule()
    for entry in schedule[:5]:
        print(entry)