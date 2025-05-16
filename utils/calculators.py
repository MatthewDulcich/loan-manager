# utils/calculators.py

from datetime import date, timedelta
from typing import List, Dict

def calculate_accrued_interest(principal: float, annual_rate: float, days: int) -> float:
    """
    Calculate accrued interest over a given number of days.
    """
    daily_rate = annual_rate / 100 / 365
    return round(principal * daily_rate * days, 2)

def calculate_monthly_payment(principal: float, annual_rate: float, term_months: int) -> float:
    """
    Calculate the fixed monthly payment for a loan.
    """
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0:
        return round(principal / term_months, 2)
    payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -term_months)
    return round(payment, 2)

def generate_amortization_schedule(
    principal: float,
    annual_rate: float,
    term_months: int,
    start_date: date,
    extra_payment: float = 0.0
) -> List[Dict]:
    """
    Generate an amortization schedule for a loan.
    """
    schedule = []
    balance = principal
    monthly_payment = calculate_monthly_payment(principal, annual_rate, term_months)
    monthly_rate = annual_rate / 100 / 12
    payment_date = start_date

    for _ in range(term_months):
        interest = round(balance * monthly_rate, 2)
        principal_payment = round(monthly_payment - interest + extra_payment, 2)
        if principal_payment > balance:
            principal_payment = balance
            monthly_payment = interest + principal_payment
        balance = round(balance - principal_payment, 2)
        schedule.append({
            "date": payment_date,
            "payment": round(monthly_payment + extra_payment, 2),
            "principal": principal_payment,
            "interest": interest,
            "balance": balance
        })
        if balance <= 0:
            break
        payment_date += timedelta(days=30)  # Approximate next month

    return schedule

def calculate_weighted_average_life(schedule: List[Dict]) -> float:
    """
    Calculate the weighted-average life (WAL) of a loan.
    """
    total_principal = sum(entry["principal"] for entry in schedule)
    if total_principal == 0:
        return 0.0
    weighted_sum = 0.0
    for i, entry in enumerate(schedule, start=1):
        weighted_sum += entry["principal"] * i
    return round(weighted_sum / total_principal, 2)

if __name__ == "__main__":
    # Test calculate_accrued_interest
    accrued = calculate_accrued_interest(1000, 5, 30)
    print(f"Accrued interest on $1000 at 5% for 30 days: {accrued}")

    # Test calculate_monthly_payment
    monthly_payment = calculate_monthly_payment(10000, 5, 60)
    print(f"Monthly payment for $10,000 at 5% over 60 months: {monthly_payment}")

    # Test generate_amortization_schedule
    from datetime import date
    schedule = generate_amortization_schedule(
        principal=10000,
        annual_rate=5,
        term_months=12,
        start_date=date(2025, 1, 1),
        extra_payment=50
    )
    print("First 3 entries of amortization schedule:")
    for entry in schedule[:3]:
        print(entry)

    # Test calculate_weighted_average_life
    wal = calculate_weighted_average_life(schedule)
    print(f"Weighted Average Life: {wal}")