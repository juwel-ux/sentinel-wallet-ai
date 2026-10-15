"""
Forecasting module - Predict future expenses and detect shortfalls.
"""

from features.accounting import get_today_transactions


def daily_average(days=7):
    """Calculate daily average spending."""
    transactions = get_today_transactions()
    if not transactions:
        return 0.0
    total = sum(tx["amount_eth"] for tx in transactions)
    return total / max(days, 1)


def forecast_monthly():
    """Forecast monthly spending based on daily average."""
    daily_avg = daily_average()
    monthly = daily_avg * 30
    print(f"\n[Forecast]")
    print(f"  Daily average: {daily_avg:.6f} ETH")
    print(f"  Projected monthly: {monthly:.6f} ETH")
    return monthly


def forecast_expense(expense_eth, savings_eth):
    """Check if a planned expense is affordable."""
    print(f"\n[Forecast] Planned expense: {expense_eth} ETH")
    print(f"  Current savings: {savings_eth} ETH")
    
    remaining = savings_eth - expense_eth
    
    if remaining < 0:
        print(f"  WARNING: Shortfall of {abs(remaining):.6f} ETH")
        return False, f"Shortfall: need {abs(remaining):.6f} ETH more"
    
    if remaining < expense_eth * 0.2:
        print(f"  CAUTION: Only {remaining:.6f} ETH remaining after expense")
        return True, f"Tight but affordable. Remaining: {remaining:.6f} ETH"
    
    print(f"  OK: Safe. Remaining: {remaining:.6f} ETH")
    return True, f"Safe. Remaining: {remaining:.6f} ETH"


def check_recurring_bills(bills_list):
    """Check upcoming recurring bills."""
    print(f"\n[Forecast] Upcoming bills:")
    total = 0
    for bill in bills_list:
        print(f"  - {bill['name']}: {bill['amount']} ETH on day {bill['day']}")
        total += bill["amount"]
    print(f"  Total upcoming: {total:.6f} ETH")
    return total
