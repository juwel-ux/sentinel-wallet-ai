"""
Advice module - Provide right/wrong financial advice based on rules.
"""

from features.accounting import get_today_transactions


def advise_purchase(amount_eth, savings_eth, purpose="purchase"):
    """Advise on a planned purchase."""
    ratio = amount_eth / savings_eth if savings_eth > 0 else float("inf")
    
    print(f"\n[Advice] {purpose}: {amount_eth} ETH")
    print(f"  Savings: {savings_eth} ETH ({ratio*100:.1f}% of savings)")
    
    if ratio > 0.5:
        advice = "NOT RECOMMENDED: Purchase exceeds 50% of savings"
        print(f"  {advice}")
        return False, advice
    
    if ratio > 0.2:
        advice = "CAUTION: Purchase exceeds 20% of savings"
        print(f"  {advice}")
        return True, advice
    
    advice = "OK: Safe purchase"
    print(f"  {advice}")
    return True, advice


def advise_savings(savings_eth, income_eth):
    """Advise on savings strategy."""
    savings_rate = savings_eth / income_eth if income_eth > 0 else 0
    
    print(f"\n[Advice] Savings rate: {savings_rate*100:.1f}%")
    
    if savings_rate < 0.1:
        advice = "LOW: Aim to save at least 10% of income"
    elif savings_rate < 0.2:
        advice = "OK: 10-20% savings rate is acceptable"
    else:
        advice = "GOOD: Above 20% savings rate is excellent"
    
    print(f"  {advice}")
    return advice


def advise_investment(investment_eth, savings_eth):
    """Advise on investment decision."""
    if investment_eth > savings_eth * 0.3:
        return False, "NOT RECOMMENDED: Investment exceeds 30% of savings"
    return True, "OK: Investment is within safe range"


def advise_debt(debt_eth, income_eth):
    """Advise on debt management."""
    ratio = debt_eth / income_eth if income_eth > 0 else float("inf")
    if ratio > 0.5:
        return "CRITICAL: Debt exceeds 50% of income. Prioritize repayment."
    if ratio > 0.3:
        return "WARNING: Debt exceeds 30% of income. Be cautious."
    return "OK: Debt level is manageable."
