"""
Budget module - Create and monitor monthly budget by category.
"""

import json
import os
from datetime import datetime


BUDGET_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "budget.json")


DEFAULT_BUDGET = {
    "monthly_income_eth": 1.0,
    "categories": {
        "food": 0.2,
        "transport": 0.1,
        "entertainment": 0.05,
        "bills": 0.15,
        "savings": 0.3,
        "other": 0.2
    }
}


def load_budget():
    """Load budget from file or use default."""
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE) as f:
            return json.load(f)
    return DEFAULT_BUDGET.copy()


def save_budget(budget):
    os.makedirs(os.path.dirname(BUDGET_FILE), exist_ok=True)
    with open(BUDGET_FILE, "w") as f:
        json.dump(budget, f, indent=2)


def set_budget(category, amount_eth):
    """Set budget for a category."""
    budget = load_budget()
    budget["categories"][category] = amount_eth
    save_budget(budget)
    print(f"[Budget] {category}: {amount_eth} ETH")


def get_budget_status():
    """Get full budget status."""
    budget = load_budget()
    total_allocated = sum(budget["categories"].values())
    remaining = budget["monthly_income_eth"] - total_allocated
    
    print(f"\n[Budget Status]")
    print(f"  Monthly income: {budget['monthly_income_eth']} ETH")
    print(f"  Total allocated: {total_allocated:.6f} ETH")
    print(f"  Unallocated: {remaining:.6f} ETH")
    print(f"  Categories:")
    for cat, amt in budget["categories"].items():
        print(f"    - {cat}: {amt} ETH")
    
    return budget


def check_category_alert(category, spent_eth):
    """Check if spending exceeds category budget."""
    budget = load_budget()
    if category not in budget["categories"]:
        return False, f"Unknown category: {category}"
    
    limit = budget["categories"][category]
    if spent_eth > limit:
        return False, f"{category} budget exceeded: {spent_eth} > {limit} ETH"
    
    return True, f"OK ({spent_eth}/{limit} ETH)"
