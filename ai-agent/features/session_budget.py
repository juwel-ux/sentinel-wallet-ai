"""
Session Budget module - Enforce cumulative spending limit per session.
"""


class SessionBudget:
    def __init__(self, session_limit_eth=0.05):
        self.session_limit = session_limit_eth
        self.spent_in_session = 0.0
        self.transactions = []
    
    def can_spend(self, amount_eth):
        """Check if amount fits within session budget."""
        if self.spent_in_session + amount_eth > self.session_limit:
            remaining = self.session_limit - self.spent_in_session
            return False, f"EXCEEDS_SESSION: remaining {remaining:.6f} ETH < {amount_eth} ETH"
        return True, "OK"
    
    def record_spend(self, amount_eth, tx_hash=""):
        """Record a successful spend."""
        self.spent_in_session += amount_eth
        self.transactions.append({
            "amount": amount_eth,
            "tx_hash": tx_hash
        })
    
    def reset(self):
        """Reset session budget."""
        self.spent_in_session = 0.0
        self.transactions = []
    
    def get_remaining(self):
        return self.session_limit - self.spent_in_session
    
    def get_status(self):
        return {
            "limit": self.session_limit,
            "spent": self.spent_in_session,
            "remaining": self.get_remaining(),
            "transactions": len(self.transactions)
        }


# Singleton
_session_budget = None


def get_session_budget(session_limit_eth=0.05):
    global _session_budget
    if _session_budget is None:
        _session_budget = SessionBudget(session_limit_eth=session_limit_eth)
    return _session_budget


def check_session_budget(amount_eth, session_limit_eth=0.05):
    """Convenience function."""
    budget = get_session_budget(session_limit_eth=session_limit_eth)
    return budget.can_spend(amount_eth)


def record_session_spend(amount_eth, tx_hash=""):
    budget = get_session_budget()
    budget.record_spend(amount_eth, tx_hash)


def reset_session_budget():
    budget = get_session_budget()
    budget.reset()
    print("[SessionBudget] Reset")


def print_session_status():
    budget = get_session_budget()
    status = budget.get_status()
    print(f"\n[SessionBudget] Limit: {status['limit']} ETH | "
          f"Spent: {status['spent']:.6f} ETH | "
          f"Remaining: {status['remaining']:.6f} ETH | "
          f"Transactions: {status['transactions']}")
